stream_query = \
        """
        {{
            user(id: "{}") {{
                streams {{
                    active
                    streamId
                    amountPerSec
                    token {{
                        address
                    }}
                    payee {{
                        address
                    }}
                }}
            }}
        }}
        """
