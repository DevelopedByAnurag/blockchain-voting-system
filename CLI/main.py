from web3 import Web3
# from web3.auto import w3

# Replace the following with your Ethereum node endpoint
web3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/SirJaLTDeoCq-UEzF0tR53qXVl1cXueW"))
private_key = "063392814689157ac8e871f99cfd65b15f855591e8b2f1a711a6456261a05dab"
account = web3.eth.account.from_key(private_key)

# Replace with the deployed smart contract address and ABI
contract_address = "0xe4F84c151646193fBc329Bb1d7b6afaec5d8E29C"
contract_abi = [
    {
      "inputs": [
        {
          "internalType": "string[]",
          "name": "candidateNames",
          "type": "string[]"
        }
      ],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "anonymous": False,
      "inputs": [
        {
          "indexed": True,
          "internalType": "address",
          "name": "voter",
          "type": "address"
        },
        {
          "indexed": True,
          "internalType": "uint256",
          "name": "candidateIndex",
          "type": "uint256"
        }
      ],
      "name": "Voted",
      "type": "event"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "candidates",
      "outputs": [
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "voteCount",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "electionAuthority",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "candidateIndex",
          "type": "uint256"
        }
      ],
      "name": "getCandidate",
      "outputs": [
        {
          "internalType": "string",
          "name": "name",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "voteCount",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getCandidateCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "getTotalVoteCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "voterAddress",
          "type": "address"
        }
      ],
      "name": "hasVoterVoted",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "candidateIndex",
          "type": "uint256"
        }
      ],
      "name": "vote",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "name": "voters",
      "outputs": [
        {
          "internalType": "bool",
          "name": "hasVoted",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]

# Load the smart contract
voting_contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def print_candidates():
    candidate_count = voting_contract.functions.getCandidateCount().call()
    print("Candidates:")
    for i in range(candidate_count):
        name, vote_count = voting_contract.functions.getCandidate(i).call()
        print(f"{i + 1}. {name} - Votes: {vote_count}")

def main():
    print("Welcome to the Voting System CLI")

    while True:
        print("\nOptions:")
        print("1. View Candidates")
        print("2. Vote")
        print("3. Check if You've Voted")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print_candidates()
        elif choice == "2":
            candidate_index = int(input("Enter the candidate index to vote: "))
            try:
                # Replace with the private key of the voter's Ethereum account
                # account = web3.eth.accounts.privateKeyToAccount(private_key)

                # Send a transaction to the smart contract
                transaction = voting_contract.functions.vote(candidate_index - 1).build_transaction({
                    "from": account.address,
                    "gas": 2000000,
                    "gasPrice": web3.to_wei(30, "gwei"),
                    "nonce": web3.eth.get_transaction_count(account.address),
                })

                signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
                transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

                print(f"Vote submitted. Transaction Hash: {transaction_hash.hex()}")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "3":
            try:
                print("hello")
                
                has_voted = voting_contract.functions.hasVoterVoted(account.address).call()
                if has_voted:
                    print("You have already voted.")
                else:
                    print("You have not voted yet.")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == "4":
            print("Exiting the Voting System CLI")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
