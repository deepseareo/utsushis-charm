import os
import sys
import tkinter as tk
from .frame_extraction import extract_unique_frames
from .charm_extraction import (
    extract_charms,
    save_charms,
    repair_invalid,
    remove_duplicates,
)
from .charm_encoding import encode_charms
from .arg_builder import build_args
from .utils import print_licenses
from .ui.AskUpdate import AskUpdate, UpdateType
from .ui.MainWindow import MainWindow
from .translator import Translator
from .resources import get_language_code, get_resource_path
from .updater import (
    ask_main_update,
    ask_language_update,
    ask_skill_update,
    ask_corrections_update,
    VersionChecker,
)

import logging

logging.basicConfig(
    filename="app.log", filemode="w", format="%(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def handle_exception(exception, value, traceback):
    logger.error(f"An error occured {exception}, {value}, {str(traceback)}")
    logger.exception(f"An error occured")
    print("An error occured", exception)


def main(args):
    if args.license:
        print_licenses()
        sys.exit(0)

    dirs_to_init = [
        get_resource_path("LOCAL_DIR"),
        get_resource_path("LOCAL_TRANSLATIONS"),
        get_resource_path("LOCAL_SKILLS"),
    ]
    for dir_to_init in dirs_to_init:
        os.makedirs(dir_to_init, exist_ok=True)

    app_language_code = get_language_code(args.app_language)
    skill_language_code = get_language_code(args.language)

    if args.console:
        run_in_console(args)

    else:
        version_checker = VersionChecker()
        main_window, translator = create_main_window(args)

        new_app_update = ask_main_update(version_checker, main_window, translator)
        new_skills_update = ask_skill_update(version_checker, main_window, translator)

        new_lang_update = ask_language_update(
            version_checker, main_window, app_language_code, translator
        )
        new_corrections_update = ask_corrections_update(
            version_checker, main_window, skill_language_code, translator
        )

        if new_lang_update:
            translator = Translator(app_language_code)
            main_window.refresh(translator)

        main_window.mainloop()


def create_main_window(args):
    app_language_code = get_language_code(args.app_language)
    translator = Translator(app_language_code)
    new_window = MainWindow(translator, args)
    new_window.report_callback_exception = handle_exception
    sys.stdout = new_window

    return new_window, translator


def run_in_console(args):
    translator = Translator()
    input_dir = args.input_dir
    frame_dir = args.frame_dir
    charm_json = args.charm_json
    charm_encoded = args.charm_encoded

    lang = get_language_code(args.language)

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(frame_dir, exist_ok=True)

    if not args.skip_frames:
        extract_unique_frames(input_dir, frame_dir, translator)

    if not args.skip_charms:
        charms = extract_charms(frame_dir, lang, translator)
        if charms.has_invalids():
            charms = repair_invalid(lang, charms, translator)
            charms = remove_duplicates(charms, mode="a")

        save_charms(charms, charm_json)
        print(f"Saved {len(charms)} charms")

    print("Encoding charms")
    encode_charms(charm_json, charm_encoded)
    print(
        'Charms encoded under "charms.encoded.txt". Use the contents of that file on the MHR Wiki armor set builder'
    )

    if not args.autoexit:
        input("Press Enter to Exit...")
