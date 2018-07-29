"""Bla."""

from collections import OrderedDict

from rest_framework import serializers
from ..base import AsyncWorker, StartJobView
from ..tools import (records_from_data_files, data_to_html_data)
from ..serializers import FileSerializer
import networkx as nx
from dnaweaver import (CommercialDnaOffer, DnaAssemblyStation, PartsLibrary,
                       PcrOutStation, DnaSourcesComparator)
from dnaweaver.reports import (JsonQuote, make_folder_report,
                               autocolor_quote_sources)

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

        def sort_suppliers(graph_data):
            supply_graph = nx.DiGraph([
                (supplier, supplier_id)
                for supplier_id, supplier_data in graph_data.items()
                for supplier in supplier_data['suppliers']
            ])
            sorted_suppliers = []
            while len(supply_graph):
                independant_suppliers = [
                    n for n in supply_graph.nodes()
                    if len(nx.ancestors(supply_graph, n)) == 0
                ]
                sorted_suppliers.extend(independant_suppliers)
                supply_graph.remove_nodes_from(independant_suppliers)
            return sorted_suppliers

        sorted_suppliers = sort_suppliers(data['graph'])
        main_id = sorted_suppliers[-1]

        suppliers_dict = {}
        for supplier_id in sorted_suppliers:
            supplier = data['graph'][supplier_id]
            supplier['parameters']["name"] = supplier["name"]
            supplier['parameters']['suppliers'] = [
                suppliers_dict[supp_id]
                for supp_id in supplier['suppliers']
            ]
            suppliers_dict[supplier_id] = {
                'commercial':  CommercialDnaOffer,
                'assembly': DnaAssemblyStation,
                'library': PartsLibrary,
                'pcr': PcrOutStation,
                'comparator': DnaSourcesComparator,
                'main': DnaSourcesComparator
            }[supplier["type"]].from_dict(supplier['parameters'])
        main = suppliers_dict[main_id]
        quote = main.get_quote(sequence, with_assembly_plan=True)
        quote.compute_full_assembly_tree()
        quote.compute_fragments_final_locations()
        json_quote = JsonQuote.from_dnaweaver_quote(quote)
        autocolor_quote_sources(json_quote)
        report_data = make_folder_report(json_quote, target='@memory')
        return {
            'quote_tree': json_quote.tree,
            'zip_file': {
                'data': data_to_html_data(report_data, 'zip'),
                'name': 'sequence_decomposition_report.zip',
                'mimetype': 'application/zip'
            },
            'success': True
        }





class GenericSolverView(StartJobView):
    serializer_class = serializer_class
    worker_class = worker_class
