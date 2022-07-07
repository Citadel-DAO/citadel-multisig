stream_query = \
        """
        {{
            user(id: "{}") {{
                streams {{
                    active
                    streamId
                    amountPerSec
                    payee {{
                        address
                    }}
                }}
            }}
        }}
        """
