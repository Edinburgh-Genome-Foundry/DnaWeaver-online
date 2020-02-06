"""Bla."""
import os
from collections import OrderedDict

from rest_framework import serializers
from ..base import AsyncWorker, StartJobView
from ..tools import (
    records_from_data_files,
    data_to_html_data,
    matplotlib_figure_to_svg_base64_data,
)
from ..serializers import FileSerializer
import dnaweaver as dw

dw.PcrExtractionStation.dna_banks = {
    "e_coli": os.path.join("app", "data", "blastdb", "e_coli", "ecoli")
}
dw.PartsLibrary.collections_by_id["EMMA"] = dict(
    library_class="golden_gate",
    fasta_file=os.path.join("app", "data", "emma_parts.fa"),
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
        graph = data["graph"]
        main = dw.DnaSupplier.from_json_data(data=graph)
        levels = main.data["levels"]
        suppliers_dict = main.data["suppliers_dict"]
        for supplier in suppliers_dict.values():
            if hasattr(supplier, "solver_kwargs"):
                supplier.memoize = True
                if levels[main.id] - levels[supplier.id] > 1:
                    logger = None
                else:
                    logger = self.logger
                supplier.solver_kwargs.update(dict(logger=logger,))
        if data["optimization"] == "cheapest_with_deadline":
            max_lead_time = data["deadline"]
        else:
            max_lead_time = None
        if data["optimization"] == "fastest_under_budget":
            max_price = data["budget"]
        else:
            max_price = None
        self.logger(message="Finding the best strategy...")
        main.prepare_network_on_sequence(sequence)
        quote = main.get_quote(
            sequence,
            max_lead_time=max_lead_time,
            max_price=max_price,
            with_assembly_plan=True,
        )
        if not quote.accepted:
            return {"accepted": False, "success": True}
        self.logger(price=quote.price)
        self.logger(lead_time=quote.lead_time)
        self.logger(message="Computing assembly details...")
        try:
            assembly_plan_report = quote.to_assembly_plan_report()
        except:
            return {
                "message": "Failed to compute details",
                "success": True,
                "accepted": True,
            }

        self.logger(message="Writing the report...")
        ax, _ = assembly_plan_report.plot_assembly_blocks(
            plot_top_assembly=False, ax=None, parts_offset=0.1, legend=True
        )
        ax.figure.set_size_inches((7, 4))
        ax.figure.subplots_adjust(bottom=0.3)
        self.logger(
            figure_data=matplotlib_figure_to_svg_base64_data(
                ax.figure, bbox_inches="tight"
            )
        )
        report_data = assembly_plan_report.write_full_report(target="@memory")

        return {
            "accepted": True,
            "assembly_tree": assembly_plan_report.plan,
            "assembly_report": {
                "data": data_to_html_data(report_data, "zip"),
                "name": "sequence_decomposition_report.zip",
                "mimetype": "application/zip",
            },
            "success": True,
        }


class GenericSolverView(StartJobView):
    serializer_class = serializer_class
    worker_class = worker_class
