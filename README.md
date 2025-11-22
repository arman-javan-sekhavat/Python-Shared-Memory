# Python-Shared-Memory
## A Python Implementation of the Shared Memory, Synchronized by the Windows Kernel Functions

* This repository contains two Python scripts, Writer and Reader. These can be used to share data in the form of NumPy arrays between two separate Python interpreters on the same machine. This implementation focuses on maximizing the transfer speed and preventing information loss during the transfer, achieved by utilizing the Windows Kernel synchronization functions.

* The corresponding communication channel is unidirectional (simplex) and consists of two nodes, the Writer and the Reader. Each of these nodes is implemented in a separate Python interpreter. Two Python classes are designed, one for each of these nodes.

Note: The Writer script must be executed before the Reader script.
