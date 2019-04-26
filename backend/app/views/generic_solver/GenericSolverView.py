"""Bla."""
import os
from collections import OrderedDict

from rest_framework import serializers
from ..base import AsyncWorker, StartJobView
from ..tools import (records_from_data_files, data_to_html_data,
                     matplotlib_figure_to_svg_base64_data)
from ..serializers import FileSerializer
import networkx as nx
from dnaweaver import (CommercialDnaOffer, DnaAssemblyStation, PartsLibrary,
                       PcrOutStation, DnaSourcesComparator)
from dnaweaver.reports import (JsonQuote, make_folder_report,
                               autocolor_quote_sources, plot_assembly_blocks)

PcrOutStation.dna_banks = {
    'e_coli': os.path.join("app", "data", "blastdb", "e_coli", "ecoli")
}

class serializer_class(serializers.Serializer):
    sequence_file = FileSerializer(allow_null=True)
    graph = serializers.JSONField()
    optimization = serializers.CharField()
    budget = serializers.FloatField()
    deadline = serializers.FloatField()

class worker_class(AsyncWorker):

    def work(self):
        self.logger(message="Reading the files...")
        data = self.data
        record = records_from_data_files([data.sequence_file])[0]
        sequence = str(record.seq)

        self.logger(message="Loading the supply graph")
        def sort_suppliers(graph_data):
            supply_graph = nx.DiGraph([
                (supplier, supplier_id)
                for supplier_id, supplier_data in graph_data.items()
                for supplier in supplier_data['suppliers']
            ])
            sorted_suppliers = []
            level = 0
            levels = {}

            while len(supply_graph):
                level += 1
                independant_suppliers = [
                    n for n in supply_graph.nodes()
                    if len(nx.ancestors(supply_graph, n)) == 0
                ]
                for supp in independant_suppliers:
                    levels[supp] = level
                sorted_suppliers.extend(independant_suppliers)
                supply_graph.remove_nodes_from(independant_suppliers)
            return sorted_suppliers, levels

        sorted_suppliers, levels = sort_suppliers(data['graph'])
        main_id = sorted_suppliers[-1]

        suppliers_dict = {}
        for supplier_id in sorted_suppliers:
            supplier_data = data['graph'][supplier_id]
            supplier_data['parameters']["name"] = supplier_data["name"]
            supplier_data['parameters']['suppliers'] = [
                suppliers_dict[supp_id]
                for supp_id in supplier_data['suppliers']
            ]
            supplier = suppliers_dict[supplier_id] = {
                'commercial':  CommercialDnaOffer,
                'assembly': DnaAssemblyStation,
                'library': PartsLibrary,
                'pcr': PcrOutStation,
                'comparator': DnaSourcesComparator,
                'main': DnaSourcesComparator
            }[supplier_data["type"]].from_dict(supplier_data['parameters'])
            if (supplier_data["type"] == 'assembly'):
                if levels[main_id] - levels[supplier_id] > 1:
                    logger = None
                else:
                    logger = self.logger
                supplier.solve_kwargs['logger'] = logger
            if (supplier_data["type"] == 'pcr'):
                supplier.pre_blast(sequence)
            supplier.memoize = True

        self.logger(message="Exploring strategies...")
        main = suppliers_dict[main_id]
        # for name, supp in suppliers_dict.items():
        #     if hasattr(supp, 'solve_kwargs') and name != main_id:
        #         supp.solve_kwargs['logger'] = None
        #         print (name, supp)

        if data['optimization'] == 'cheapest_with_deadline':
            max_lead_time = data['deadline']
        else:
            max_lead_time = None
        if data['optimization'] == 'fastest_under_budget':
            max_price = data['budget']
        else:
            max_price = None
        quote = main.get_quote(
            sequence,
            max_lead_time=max_lead_time,
            max_price=max_price,
            with_assembly_plan=True)
        if not quote.accepted:
            return {
                'accepted': False,
                'success': True
            }
        self.logger(price=quote.price)
        self.logger(lead_time=quote.lead_time)
        self.logger(message="Computing assembly details...")
        try:
            quote.compute_full_assembly_tree()
            quote.compute_fragments_final_locations()
        except:
            json_quote = JsonQuote.from_dnaweaver_quote(quote)
            return {
               'message': 'Failed to compute details',
               'success': True,
               'accepted': True,
               'assembly_tree': json_quote.tree
            }

        self.logger(message="Writing the report...")
        json_quote = JsonQuote.from_dnaweaver_quote(quote)
        autocolor_quote_sources(json_quote)
        report_data = make_folder_report(json_quote, target='@memory')

        ax, _ = plot_assembly_blocks(json_quote, backend="matplotlib",
                                     plot_top_assembly=False,
                                     ax=None, parts_offset=0.1, legend=True)
        ax.figure.set_size_inches((7, 4))
        ax.figure.subplots_adjust(bottom=0.3)
        return {
            'accepted': True,
            'assembly_tree': json_quote.tree,
            'assembly_figure_data': matplotlib_figure_to_svg_base64_data(
                ax.figure, bbox_inches='tight'),
            'assembly_report': {
                'data': data_to_html_data(report_data, 'zip'),
                'name': 'sequence_decomposition_report.zip',
                'mimetype': 'application/zip'
            },
            'success': True
        }





class GenericSolverView(StartJobView):
    serializer_class = serializer_class
    worker_class = worker_class
