"""
The main entry point for the application.
"""

import sys

from clingo import Control
from .utils.logging import configure_logging, get_logger
from .utils.parser import get_parser
from .transformers.transformer_pipeline import (
    AbductionPipeline,
    ModelSupportPipeline,
)
from importlib_resources import files
import os


def main() -> None:
    """
    Run the main function.
    """
    parser = get_parser()
    args = parser.parse_args()
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())

    log = get_logger("main")

    domain_file_paths = [f.name for f in args.files]
    domain_base_path = os.path.dirname(domain_file_paths[0])
    output_dir = os.path.join(domain_base_path, "out")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    abduction_prg = AbductionPipeline().parse_files(domain_file_paths)
    with open(os.path.join(domain_base_path, "out", "abduction.lp"), "w") as f:
        f.write(abduction_prg)
        log.debug("Abduction encoding saved in " + f.name)

    support_prg = ModelSupportPipeline().parse_files(domain_file_paths)
    with open(os.path.join(domain_base_path, "out", "support.lp"), "w") as f:
        f.write(support_prg)
        log.debug("Support encoding saved in " + f.name)

    ctl = Control(["0", "--opt-mode=optN"])
    ctl.add("base", [], abduction_prg)
    ctl.add("base", [], support_prg)
    for f in args.explanation_config:
        ctl.load(f.name)
    base_encoding = files("asplain.encodings").joinpath("base.lp")
    ctl.load(str(base_encoding))
    ctl.ground([("base", [])])
    # TODO save the rules somewhere (the mapping from id to rule)
    contrastive_explanations = []
    with ctl.solve(yield_=True) as handle:
        for m in handle:
            # TODO check how to avoid having double models
            if not m.optimality_proven:
                log.debug("Skipping non optimal model")
                continue
            contrastive_explanations.append([str(s) for s in m.symbols(atoms=True)])
            log.debug("----- Expanation %s", m.number)
            log.debug(m)


if __name__ == "__main__":
    main()
