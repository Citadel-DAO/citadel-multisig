stream_query = \
        """
        {
            user(id: "{safe}") {
                streams {
                    streamId
                    amountPerSec
                    payee {
                        address
                    }
                }
            }
        }
        """