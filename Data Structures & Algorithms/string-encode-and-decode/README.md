# Encode and Decode Strings

An industrial-grade, low-overhead string serialization mechanism utilizing the **Length-Prefix Selection / Chunked Transfer Encoding** algorithm. This protocol resolves the **Delimiter Collision Problem** natively without structural character escaping, character replacement, or third-party serialization libraries (e.g., JSON, Protocol Buffers).

---

## 🛠️ The Architecture: Length-Prefix Selection

When designing a network protocol or data transmission layer to pack an arbitrary array of strings into a single string vector, standard delimiter configurations (such as splitting by `,`, `:`, or `\n`) fail whenever the raw text naturally contains that delimiter. 

### Core Protocol Mechanics
Instead of modifying or scanning the internal text bytes to escape illegal symbols, our approach encapsulates every single string inside a self-contained, length-prefixed packet:

$$\text{Packet Structure} = [\text{Length in Characters}] + [\text{Gateway Delimiter (":")}] + [\text{Raw Data payload}]$$

```
Input Array:   ["hello:world", "", "🎨"]
                |              |   |
Packet 1:       11:hello:world |   |
Packet 2:                      0:  |
Packet 3:                          1:🎨

Final Stream:  "11:hello:world0:1:🎨"
```

### Protocol Advantages
* **Immunity to Delimiter Collision:** The gateway colon (`:`) is only used as a structural token to separate metadata from payload. The decoder never reads data-level colons because its parsing window hops dynamically over the payload byte counts.
* **Binary-Safe & Unicode Resilient:** Handles arbitrary text characters, multiline carriage returns (`\n`), null bytes, and multibyte Unicode characters (such as emojis) safely.
* **Zero Padding Overhead:** Highly deterministic encoding string layout that tracks metadata using standard Base-10 scaling lengths.

---

## 💻 Python Source Implementation

```python
class StringCodec:
    def encode(self, strs: list[str]) -> str:
        """Encodes an ordered list of strings into a single contiguous transmission string.
        
        Time Complexity: O(N) where N is the aggregate character count across all strings.
        Space Complexity: O(N) to assemble the final unified text buffer.
        """
        # Uses an efficient generator expression inside join to minimize string allocations
        return "".join(f"{len(s)}:{s}" for s in strs)

    def decode(self, s: str) -> list[str]:
        """Decodes a length-prefixed unified string back into its original array composition.
        
        Time Complexity: O(N) where N is the length of the string 's'.
        Space Complexity: O(1) auxiliary space (excluding the returned result array allocations).
        """
        result: list[str] = []
        i: int = 0
        string_len: int = len(s)
        
        while i < string_len:
            # Step 1: Scan forward from the current cursor to find the metadata gateway
            colon_index = s.find(':', i)
            
            # Step 2: Slice the Base-10 digits and cast them to a computational integer
            length = int(s[i:colon_index])
            
            # Step 3: Compute exact slice indices for target payload window extraction
            start_payload = colon_index + 1
            end_payload = start_payload + length
            
            # Step 4: Extract the exact payload segment and update the tracking state array
            result.append(s[start_payload:end_payload])
            
            # Step 5: Advance cursor directly past the extracted payload window
            i = end_payload
            
        return result
```

---

## 🔬 Mathematical & Trace Complexity Analysis

### Time Complexity

* **Encoding Phase: $\mathcal{O}(N)$**
  The encoder iterates through the array of length $K$, scanning each character to measure its string size exactly once. The underlying implementation invokes a C-level buffer generation routine which chains strings linearly relative to total character payload data.
* **Decoding Phase: $\mathcal{O}(N)$**
  The scanner cursor index $i$ processes the serialized string cleanly from left to right. Inside the `while` loop block:
  1. `s.find()` scans forward only until the next colon.
  2. The payload extraction slices a specific substring chunk window of scale length $L$.
  Each element in the stream is inspected bounded by a constant factor $\le 2$, executing in strict linear $\mathcal{O}(N)$ execution time.

### Space Complexity

* **Auxiliary Space: $\mathcal{O}(1)$**
  The runtime footprint relies exclusively on a sequence of primitive stack tracking pointers (`i`, `colon_index`, `length`, `start_payload`, `end_payload`). No dynamic structures or recursive context tracking frames are allocated relative to input scale.
* **Data Output Space: $\mathcal{O}(N)$**
  Requires allocating memory buffers proportional to the original input volume to preserve the output serialization representations or list objects.

---

## 🔍 State Matrix & Invariant Tracing

### State Invariant Visual Tracing
For a combined serialization payload: `"4:code3:cat"`

| Iteration | Initial Pointer ($i$) | Found Colon (`colon_index`) | Text Slice ($s[i:\text{colon}]$) | Cast Integer (`length`) | Target Data Window | Updated Pointer ($i$) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Init** | `0` | — | — | — | — | — |
| **Loop 1** | `0` | `1` | `"4"` | `4` | $s[2:6]$ &rarr; `"code"` | `6` |
| **Loop 2** | `6` | `7` | `"3"` | `3` | $s[8:11]$ &rarr; `"cat"` | `11` |
| **Exit** | `11` | — | — | — | — | Loop Terminates (`11 == 11`) |

### Edge Case State Table

| Test Boundary Context | Source Input Data Array | Serialized Network String | Decoder Processing Safety Variant |
| :--- | :--- | :--- | :--- |
| **Standard Text Input** | `["cat", "tree", "dog"]` | `"3:cat4:tree3:dog"` | Standard sequentially clean boundaries. |
| **Internal Delimiter Collision** | `["hello:world", "12:30"]` | `"11:hello:world5:12:30"` | The decoder bypasses internal data colons because it indexes forward strictly using precalculated size metrics. |
| **Empty Node Arrays** | `["", "🎨", "A\nB"]` | `"0:1:🎨3:A\nB"` | Correctly maps zero-length arrays (`"0:"`) and handles single multiline or multi-byte unicode emojis. |
| **Empty Input Collection** | `[]` | `""` | Evaluates cleanly on loop execution entry step (`0 < 0` breaks instantly). |