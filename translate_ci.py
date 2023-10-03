import jinja2
import os
import sys
import pathlib
from os import path
import tomllib as toml
import argparse
from colorama import Fore

TRANSLATION_DIR = "./docs"
SNIPPET_DIR = "./docs/snippets/"
# files to be ignored when traversing the TRANSLATION_DIR
IGNORE_FILES = ["CNAME", "assets", "stylesheets", "snippets"]

# dict[language][chapter][snippet_name]
SnippetsDict = dict[str, dict[str, dict[str, str]]]

# dict[chapter][template_path]
TemplateDict = dict[str, dict[str, list[str]]]


def main() -> None:
    parser = argparse.ArgumentParser(
            prog="translate_ci",
            description="expands markdown templates into their respective translations",)
    parser.add_argument('-y', '--assumeyes', help="runs script without confirmation", action="store_true")
    args = parser.parse_args()
    if not args.assumeyes:
        print(Fore.RED + f"WARNING: All translations in {TRANSLATION_DIR} will be expanded and overwritten")
        if input(Fore.RESET + "Do you want to proceed? [Yes, I want to proceed!, N] ") != "Yes, I want to proceed!":
            return

    template_dict: TemplateDict = get_template_dict()
    snippets_dict: SnippetsDict = get_rendered_snippets_dict(template_dict)

    # render files with translations
    for language, chapters in snippets_dict.items():
        for chapter in chapters:
            try:
                language_dir = path.join(TRANSLATION_DIR, language)
                for markdown in os.listdir(language_dir):
                    markdown = path.join(language_dir, markdown)
                    with open(markdown, "r+") as md_file:
                        md_templ = jinja2.Template(md_file.read())
                        md_expanded = md_templ.render(
                            snippets_dict[language][chapter])
                        md_file.seek(0)
                        md_file.write(md_expanded)

            except FileNotFoundError:
                print(
                    f"Error: No snippets have been provided for {language}", file=sys.stderr)


# renders snippets and inserts them into a dictionary with the following structure
# structure of the returned dictionary: dict[language][chapter][snippet_name]
def get_rendered_snippets_dict(template_dict: TemplateDict) -> SnippetsDict:
    snippets_dict: dict[str, dict[str, dict[str, str]]] = dict()

    # temporary dictionary holding all snippets that don't need to be rendered for each language
    snippets_dict["no_translation"] = dict()

    # iterates through templates and renders them for each language
    for chapter, templates in template_dict.items():

        for template, translations in templates.items():
            snippet_name = pathlib.Path(template).parent.stem

            with open(template, "r") as template_file:
                if len(translations) == 0:
                    if chapter not in snippets_dict["no_translation"]:
                        snippets_dict["no_translation"][chapter] = dict()
                    snippets_dict["no_translation"][chapter][snippet_name] = template_file.read()
                    continue

                templ = jinja2.Template(template_file.read())
                for translation in translations:
                    with open(translation, "r") as translation_toml:
                        data = toml.loads(translation_toml.read())
                        language = pathlib.Path(translation).stem
                        if language not in snippets_dict:
                            snippets_dict[language] = dict()
                            snippets_dict[language][chapter] = dict()
                        snippets_dict[language][chapter][snippet_name] = templ.render(data)

    # snippets with no translations are copied to all chapter translations
    # this is necessary as Jinja2 cannot do partial templating, that means that 
    # unless all data is available in the first run the templates will be made as empty
    # thus being unable to render the other half of the data
    for language in snippets_dict:
        if language == "no_translation": continue

        for chapter in snippets_dict[language]:
            for chapter_raw, snippets in snippets_dict["no_translation"].items():
                if chapter == chapter_raw:
                    for snippet_name in snippets:
                        snippets_dict[language][chapter][snippet_name] = snippets_dict["no_translation"][chapter][snippet_name]

    del snippets_dict["no_translation"]

    # copies rendered template from english to other languages if there's no rendered translation for them
    for language in snippets_dict:
        if language == 'en': continue

        for chapter, snippets in snippets_dict['en'].items():
            for snippet in snippets:
                if snippet not in snippets_dict[language][chapter]:
                    snippets_dict[language][chapter][snippet] = snippets_dict['en'][chapter][snippet]

    return snippets_dict


# returns a dictionary in TemplateDict[Chapter][TemplateFile]
# where the chapter is the chapter name and the template file the path for the snippet
def get_template_dict() -> TemplateDict:
    translation_dict: dict[str, dict[str, list[str]]] = dict()
    for chapter in os.listdir(SNIPPET_DIR):
        chapter_path = path.join(SNIPPET_DIR, chapter)
        translation_dict[chapter] = dict()

        for section in os.listdir(chapter_path):
            section_path = path.join(chapter_path, section)
            section_files = os.listdir(section_path)

            # figure out which file is the snippet template
            template_file = ""
            for snippet in section_files:
                if snippet.endswith(".zig"):
                    template_file = path.join(section_path, snippet)
                    break

            translation_dict[chapter][template_file] = []
            # initializes dictionary with values such that
            # key: is the path for the corresponding template file (the snippet)
            # value: is a list of paths for the translation TOMLs
            for translation in section_files:
                translation_path = path.join(section_path, translation)
                if translation.endswith(".zig") or not translation.endswith(".toml"):
                    continue
                translation_dict[chapter][template_file].append(translation_path)
    return translation_dict


if __name__ == "__main__":
    main()
