"""
The main entry point for the application.
"""

import sys

from clingo import Control, clingo_main

from .app import AsplainApp


def main() -> None:
    """
    Run the main function.
    """
    clingo_main(AsplainApp(sys.argv[0]), sys.argv[1:])
    sys.exit()
    # parser = get_parser()
    # args = parser.parse_args()
    # configure_logging(sys.stderr, args.log, sys.stderr.isatty())

    # log = get_logger("main")

    # domain_file_paths = [f.name for f in args.files]
    # domain_base_path = os.path.dirname(domain_file_paths[0])
    # output_dir = os.path.join(domain_base_path, "out")
    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    # abduction_prg = AbductionPipeline().parse_files(domain_file_paths)
    # with open(os.path.join(domain_base_path, "out", "abduction.lp"), "w") as f:
    #     f.write(abduction_prg)
    #     log.info("Abduction encoding saved in " + f.name)

    # support_prg = ModelSupportPipeline().parse_files(domain_file_paths)
    # with open(os.path.join(domain_base_path, "out", "support.lp"), "w") as f:
    #     f.write(support_prg)
    #     log.info("Support encoding saved in " + f.name)

    # ctl = Control(["0", "--opt-mode=optN"])
    # ctl.add("base", [], abduction_prg)
    # ctl.add("base", [], support_prg)
    # for f in args.explanation_config:
    #     ctl.load(f.name)
    # with path("asplain.encodings", "base.lp") as base_encoding:
    #     ctl.load(str(base_encoding))
    # ctl.ground([("base", [])])
    # # TODO save the rules somewhere (the mapping from id to rule)
    # contrastive_explanations = []
    # with ctl.solve(yield_=True) as handle:
    #     for m in handle:
    #         if not m.optimality_proven:
    #             continue
    #         symbols = [str(s) for s in m.symbols(atoms=True)]
    #         contrastive_explanations.append(symbols)
    #         log.info("----- Expanation %s", m.number)
    #         log.info(m)
    #         viz_explanation(symbols, directory=output_dir, name_format=f"contrastive-ex-{m.number}")


if __name__ == "__main__":
    main()
