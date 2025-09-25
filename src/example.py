from agents.manager_agent import execute as execute_manager

# Example
part_number = "CL10C330JB8NNNC"
supplier = "Mouser Electronics"
additional_context = "CAP.CER.SMD 0603 33PF 50V 5% C0G"


response = execute_manager(part_number, supplier, additional_context)


print(
    "============================================================================================================="
)
print("FINISHED")
print("Result: ")
print(response)
