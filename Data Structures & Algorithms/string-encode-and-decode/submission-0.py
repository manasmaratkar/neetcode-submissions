class Solution:

    def encode(self, strs: List[str]) -> str:
        encoded_string = []
        
        for s in strs:
            # Format: <length>:<string>
            encoded_string.append(f"{len(s)}:{s}")
        
        return "".join(encoded_string)

    def decode(self, s: str) -> list[str]:

        result = []
        i = 0

        while i < len(s):
            
            # Find the colon that separates the length from the string
            colon_index = s.find(':', i)

            # Extract the length of the string
            length_of_string = int(s[i:colon_index])

            start_of_string_index = colon_index + 1
            end_of_string_index = start_of_string_index + length_of_string

            # Extract the actual string using the known length
            result.append(s[start_of_string_index:end_of_string_index])

            #Move the pointer to the start of the next length-prefix
            i = end_of_string_index

        return result
