from agents.app import manager_agent
from schemas.api_schemas import SingleClassificationRequest

# Example
data: SingleClassificationRequest = {
    "partnumber": "CL10C330JB8NNNC",
    "supplier": "Mouser Electronics",
    "additional_context": "CAP.CER.SMD 0603 33PF 50V 5% C0G",
}


response = manager_agent(channel="foo", job_id=1, data=data)


print(
    "============================================================================================================="
)
print("FINISHED")
print("Result: ")
print(response)
