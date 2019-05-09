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
                       PcrOutStation, DnaSourcesComparator,
                       supply_network_from_json)
from dnaweaver.reports import (JsonQuote, make_folder_report,
                               autocolor_quote_sources, plot_assembly_blocks)

PcrOutStation.dna_banks = {
    'e_coli': os.path.join("app", "data", "blastdb", "e_coli", "ecoli")
}
PartsLibrary.collections_by_id['EMMA'] = dict(
    library_class='golden_gate',
    fasta_file=os.path.join("app", "data", "emma_parts.fa")
)

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
        graph = data['graph']
        levels, suppliers_dict, main_id = supply_network_from_json(graph)
        main = suppliers_dict[main_id]
        for supplier in suppliers_dict.values():
            if hasattr(supplier, 'solver_kwargs'):
                supplier.memoize = True
                if levels[main_id] - levels[supplier.id] > 1:
                    logger = None
                else:
                    logger = self.logger
                supplier.solver_kwargs.update(dict(
                    logger=logger,
                ))
        if data['optimization'] == 'cheapest_with_deadline':
            max_lead_time = data['deadline']
        else:
            max_lead_time = None
        if data['optimization'] == 'fastest_under_budget':
            max_price = data['budget']
        else:
            max_price = None
        self.logger(message="Finding the best strategy...")
        main.prepare_network_on_sequence(sequence)
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
        ax, _ = plot_assembly_blocks(json_quote, backend="matplotlib",
                                     plot_top_assembly=False,
                                     ax=None, parts_offset=0.1, legend=True)
        ax.figure.set_size_inches((7, 4))
        ax.figure.subplots_adjust(bottom=0.3)
        self.logger(figure_data=matplotlib_figure_to_svg_base64_data(
                ax.figure, bbox_inches='tight'))
        report_data = make_folder_report(json_quote, target='@memory')
        
        return {
            'accepted': True,
            'assembly_tree': json_quote.tree,
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
