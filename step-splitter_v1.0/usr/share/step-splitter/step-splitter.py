import os
import shutil

import FreeCAD
import Import


def split_step(file_path):
    # Check if file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return

    # Copy the original file and append "_combined"
    file_path_combined = file_path.replace(".STEP", "_combined.STEP")
    shutil.copyfile(file_path, file_path_combined)

    # Load the original STEP file
    doc = FreeCAD.newDocument()
    Import.insert(file_path, doc.Name)

    # Iterate over each object in the document
    for obj in doc.Objects:
        if obj.TypeId == "Part::Feature":
            # Create a new document for each shape
            single_doc = FreeCAD.newDocument()
            single_obj = single_doc.addObject("Part::Feature", obj.Name)
            single_obj.Shape = obj.Shape

            # Generate a safe filename
            output_filename = f"{obj.Label}.step"
            Import.export([single_obj], output_filename)
            print(f"Exported: {output_filename}")

            # Clean up
            FreeCAD.closeDocument(single_doc.Name)

    # Close the original document
    FreeCAD.closeDocument(doc.Name)


def main():
    # ask for the file path using input
    file_path = input()
    split_step(file_path)


main()
