# EL-SPICE
### Efficient Language - Simulation Program with Integrated Circuit Emphasis

    pip install elspice

EL-Spice is [efficient-language](https://quantumgravityresearch.org/portfolio/principle-of-efficient-language/) based analog electronic circuit simulator. The simulated circuit is created from an expression, then required mathematical operations are applied. Overall, simulation is done. 
The lingual expression is a geometric code, describes an edge connected to points, which component lies in the edge and what is SI unit magnitude associated with the component. For example:

    (0,0) (0,1) R 5M;
This means that a 5 MΩ resistor is connected between points (0,0) and (0,1). Points are not necessarily 2D, it can be in any dimension. Each identifier follows each other by a space. Each component follows the other by a semicolon(**;**)

    (0,0) (0,1) I 2m;(0,1) (1,1) R 1K;(1,1) (0,0) R 2K;
   This time, a current source of 2mA is connected with two resistors; one them is 1KΩ, other is 2KΩ. Wires don't have any parameter.
   

    (0,0) (0,1) -;
  In summary, all components and usage scheme is listed below:
  

    (0,0) (0,1) -;
    (0,0) (0,1) V 5;
    (0,0) (0,1) I 2.3m;
    (0,0) (0,1) R 3.3M;
    (0,0) (0,1) C 4.7p;
    (0,0) (0,1) L 3.4u;
### RLC Circuit(ω=10<sup>7</sup>)

    (1,0) (1,1) V 5;(1,1) (0,1) C 2n;
    (0,1) (0,0) L 5u;(1,0) (0,0) R 5;

### Usage
 1. Firstly define your circuit with <code>circ = elspice.Circuit(D)</code> where D is number of dimensions.
 2. Create a string of circuit expression with the efficient language and AC frequency. If the circuit is DC, then just write 0 or nothing, it is default to 0. `circ.decode(string_of_circuit, frequency)`
 3. Get node voltages by calling `circ.nodes()`
 4. You can export each node voltage `circ.node_voltages()`. It returns an array and a dictionary describes that which index of array is which node.

Overall

    import elspice
    circ=circ = elspice.Circuit(D)
    
    string_of_circuit="""(1,0) (1,1) V 5;(1,1) (0,1) C 2n;
    (0,1) (0,0) L 5u;(1,0) (0,0) R 5;"""
    
    circ.decode(string_of_circuit, 1591549.430)
    circ.nodes()
Output

    Node Voltages:
    (1, 0): 0V 0°
    (1, 1): 5.0 V  -1.3232932312128532e-46 °
    (0, 1): 50.24937807687795 V  84.28940752087149 °
    (0, 0): 4.999999999999999 V  6.616466159068361e-07 °
