stream_query = \
        """
        {
            user(id:) {
                streams {
                    active
                    streamId
                    amountPerSec
                    payee {
                        address
                    }
                }
            }
        }
        """

def construct_query(address):
    # str.format doesnt work nicely with all the {} in query
    split = stream_query.split("id:")
    split.insert(1, f'id: "{address.lower()}"')
    return "".join(split)
