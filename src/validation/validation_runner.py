from .validator import PipelineValidator


class ValidationRunner:

    def run(self):

        missing = PipelineValidator.validate()

        if missing:

            print("\nValidation Failed\n")

            print("Missing Files:")

            for file in missing:

                print(file)

            return False

        print("\nAll Pipeline Outputs Validated Successfully.\n")

        return True