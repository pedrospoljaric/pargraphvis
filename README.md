# ParGraphVis

Parallel program visualization and performance analysis tools have a high cost of development. As a consequence, there are many of these tools that are proprietary what makes difficult their adoption by the general community. This work introduces the use of general purpose open software for visualization and characterization of parallel programs. In particular, the use of an open graph visualization tool is presented as a case study for the dynamic communication characterization of a NAS parallel benchmark. The results show that a general purpose open graph tool could be used to analyze some important aspects related to the communication of parallel message passing programs.

In order to generate a dynamic graph file from a trace log file, the program is to be run as follows:

> python pargraphvis.py trace_file.trace

This will make the program begin to generate a gexf extension file, which describes the graph variation during the time limited by the trace file. Those changes on the graph are made out of the message exchanges between the cluster nodes. The gexf file can then bem openned with graph visualization platforms such as [Gephi] (https://gephi.org/).
