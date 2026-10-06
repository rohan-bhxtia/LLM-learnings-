from semantic_search import semantic_search
from sentence_transformers import SentenceTransformer

docs = [
    """
    The supplier agrees to provide the services described in this agreement according to the specifications and timelines agreed upon by both parties.
    The supplier must maintain appropriate standards of quality while delivering the services to the customer.
    The customer agrees to provide the supplier with all information reasonably required to perform the services.
    The supplier must notify the customer about significant delays that could affect agreed delivery dates.
    If a delay is caused by circumstances outside the reasonable control of either party, the parties should discuss an appropriate adjustment to the delivery schedule.
    """,

    """
    All invoices issued by the supplier must be paid by the customer within 45 days of receiving the invoice.
    If an invoice is disputed, the customer must notify the supplier in writing and explain the reason for the dispute.
    Undisputed portions of an invoice must still be paid within the agreed payment period.
    Records relating to invoices and payments should be retained for the period required by applicable law.
    """,

    """
    The supplier may terminate this agreement by providing the customer with at least 30 days written notice.
    The customer may also terminate the agreement by providing 30 days written notice to the supplier.
    Either party may terminate the agreement immediately if the other party commits a material breach and fails to correct that breach.
    Termination of the agreement does not remove any payment obligations that became due before the termination date.
    The agreement may be renewed if both parties agree to extend the contract before the current term expires.
    """,

    """
    Confidential information received from the customer must not be disclosed to third parties without prior written permission.
    The supplier must use reasonable security measures to protect confidential business information.
    Employees working on the customer account may access confidential information only when necessary for their responsibilities.
    The supplier must notify the customer if it becomes aware of an unauthorized disclosure of confidential information.
    The parties agree that confidential information does not include information that is already publicly available.
    """,

    """
    The supplier may use subcontractors to perform certain services only when permitted by the agreement.
    Any subcontractor used by the supplier must comply with the confidentiality and security obligations of this agreement.
    The supplier remains responsible for the actions of its approved subcontractors.
    The supplier must maintain appropriate records relating to the services provided under this agreement.
    The customer may request reasonable documentation showing that contractual obligations are being fulfilled.
    """,

    """
    Employees of the supplier may work remotely when the arrangement has been approved by their manager and does not affect service delivery.
    Remote employees must continue to follow all company security policies while working outside the office.
    The customer must provide reasonable access to systems and information required for troubleshooting and support.
    The supplier is responsible for correcting material defects in the services identified during the agreed support period.
    """,

    """
    Neither party may assign this agreement to another organization without the prior written consent of the other party, except in certain permitted corporate transactions.
    Any changes to the agreement must be documented in writing and approved by authorized representatives of both parties.
    The parties agree to cooperate in good faith to resolve disputes relating to the services.
    If the parties cannot resolve a dispute through discussion, they may use the dispute resolution process specified in the agreement.
    The governing law and jurisdiction for this agreement are determined by the provisions stated in the contract.
    """,

    """
    The supplier must return confidential information belonging to the customer after the agreement ends.
    The obligations relating to confidentiality, payment, intellectual property, and outstanding liabilities may continue after termination.
    Termination of the agreement does not remove any payment obligations that became due before the termination date.
    """
]
model = SentenceTransformer("all-MiniLM-L6-v2")
doc_vectors = model.encode(docs)

while True:
    query = input("Ask your question (type 'stop' to quit): ").strip()
    if query.lower() == "stop":
        break
    if not query:          #we need the code to still running after doing an empty enter press.
        continue

    for score, doc in semantic_search(docs,doc_vectors, query,1):
        print(f"\nScore: {score:.3f}") # this 3f means that i need only 3 numbers after decimal
        print(doc.strip())             # removed faltu ka space 
        print()                        # this print is just for the space between my output and next ques input