#!/usr/bin/env python

# encoding: utf-8

"""
Python and RDF Utils for OntoSPy

Copyright (c) 2010 __Michele Pasin__ <michelepasin.org>. All rights reserved.

"""



import rdflib
DEFAULT_LANGUAGE = "en"





class QueryHelper(object):
	"""
	A bunch of RDF queries 
	"""
	
		
	def __init__(self, rdfgraph):
		super(QueryHelper, self).__init__() 
		self.rdfgraph = rdfgraph
		
		# Bind a few prefix, namespace pairs for easier sparql querying
		self.rdfgraph.bind("rdf", rdflib.namespace.RDF)
		self.rdfgraph.bind("rdfs", rdflib.namespace.RDFS)
		self.rdfgraph.bind("owl", rdflib.namespace.OWL)
		self.rdfgraph.bind("skos", rdflib.namespace.SKOS)
		
		
	def getOntology(self):
		qres = self.rdfgraph.query(
			"""SELECT DISTINCT ?x
			   WHERE {
				  ?x a owl:Ontology
			   }""")
		return list(qres)


	def entityTriples(self, aURI):
		""" builds all triples for an entity"""

		aURI = str(aURI)
		qres = self.rdfgraph.query(
			  """CONSTRUCT {<%s> ?y ?z }
				 WHERE {
					 { <%s> ?y ?z } 
				 }	 
				 """ % (aURI, aURI ))
		return list(qres)
		
	# def _getAllClassesTEST(self):
	#	qres = self.rdfgraph.query(
	#		  """SELECT DISTINCT ?x
	#			# TEST
	#			 WHERE {
	#				 { ?x a owl:Class }
	#			 }
	#			 """)
	#	return list(qres)		 
		
		
	def getAllClasses(self):
		"""
		by default, obscure all RDF/RDFS/OWL/XML stuff
		"""
		qres = self.rdfgraph.query(
			  """SELECT DISTINCT ?x ?c
				 WHERE {
						 { 
							 { ?x a owl:Class } 
							 union 
							 { ?x a rdfs:Class }
							 union 
							 { ?x rdfs:subClassOf ?y }
							 union 
							 { ?z rdfs:subClassOf ?x }
							 union 
							 { ?y rdfs:domain ?x }
							 union 
							 { ?y rdfs:range ?x } 
						 } . 
						 
						 ?x a ?c
					 
					 FILTER(
					   !STRSTARTS(STR(?x), "http://www.w3.org/2002/07/owl")
					   && !STRSTARTS(STR(?x), "http://www.w3.org/1999/02/22-rdf-syntax-ns")
					   && !STRSTARTS(STR(?x), "http://www.w3.org/2000/01/rdf-schema")
					   && !STRSTARTS(STR(?x), "http://www.w3.org/2001/XMLSchema")
					   && !STRSTARTS(STR(?x), "http://www.w3.org/XML/1998/namespace")
					   && (!isBlank(?x))
					   ) .
				 }	 
				 ORDER BY  ?x
				 """)
		return list(qres)


	#legacy
	
	def getAllClassesFromInstancesToo(self):
		"""
		by default, obscure all RDF/RDFS/OWL/XML stuff
		NOTE: this is more expensive!
		
		added: { ?y rdf:type ?x } 
		"""
		qres = self.rdfgraph.query(
			  """SELECT DISTINCT ?x ?c
				 WHERE {
						 { 
							 { ?x a owl:Class } 
							 union 
							 { ?x a rdfs:Class }
							 union 
							 { ?x rdfs:subClassOf ?y }
							 union 
							 { ?z rdfs:subClassOf ?x }
							 union 
							 { ?y rdf:type ?x } 
							 union 
							 { ?y rdfs:domain ?x }
							 union 
							 { ?y rdfs:range ?x } 
						 } . 
				 
						 ?x a ?c
			 
					 FILTER(
					   !STRSTARTS(STR(?x), "http://www.w3.org/2002/07/owl")
					   && !STRSTARTS(STR(?x), "http://www.w3.org/1999/02/22-rdf-syntax-ns")
					   && !STRSTARTS(STR(?x), "http://www.w3.org/2000/01/rdf-schema")
					   && !STRSTARTS(STR(?x), "http://www.w3.org/2001/XMLSchema")
					   && !STRSTARTS(STR(?x), "http://www.w3.org/XML/1998/namespace")
					   && (!isBlank(?x))
					   ) .
				 }	 
				 ORDER BY  ?x
				 """)
		return list(qres)
		

	def getClassDirectSupers(self, aURI):
		aURI = str(aURI)
		qres = self.rdfgraph.query(
			  """SELECT DISTINCT ?x
				 WHERE {
					 { <%s> rdfs:subClassOf ?x }  
					 FILTER (!isBlank(?x))
				 } ORDER BY ?x	  
				 """ % (aURI))
		return list(qres)


	def getClassDirectSubs(self, aURI):
		""" 
		2015-06-03: currenlty not used, inferred from above
		"""
		aURI = str(aURI)
		qres = self.rdfgraph.query(
			  """SELECT DISTINCT ?x
				 WHERE {
					 { ?x rdfs:subClassOf <%s> } 
					 FILTER (!isBlank(?x))
				 }	 
				 """ % (aURI))
		return list(qres)
		
	def getClassAllSupers(self, aURI):
		""" 
		note: requires SPARQL 1.1 
		2015-06-04: currenlty not used, inferred from above
		"""
		aURI = str(aURI)
		try:
			qres = self.rdfgraph.query(
				  """SELECT DISTINCT ?x
					 WHERE {
						 { <%s> rdfs:subClassOf+ ?x } 
						 FILTER (!isBlank(?x))
					 }	 
					 """ % (aURI))
		except:
			printDebug("... warning: the 'getClassAllSupers' query failed (maybe missing SPARQL 1.1 support?)")
			qres = []
		return list(qres)	


	def getClassAllSubs(self, aURI):
		"""	 
		note: requires SPARQL 1.1	
		2015-06-04: currenlty not used, inferred from above
		"""
		aURI = str(aURI)
		try:
			qres = self.rdfgraph.query(
				  """SELECT DISTINCT ?x
					 WHERE {
						 { ?x rdfs:subClassOf+ <%s> } 
						 FILTER (!isBlank(?x))
					 }	 
					 """ % (aURI))
		except:
			printDebug("... warning: the 'getClassAllSubs' query failed (maybe missing SPARQL 1.1 support?)")
			qres = []
		return list(qres)	
	
	
	# NOTE this kinf of query could be expanded to classes too!!! 
	def getAllProperties(self):
		qres = self.rdfgraph.query(
			  """SELECT ?x ?c WHERE {
						{
							{ ?x a rdf:Property } 
							 UNION 
							 { ?x a owl:ObjectProperty }
							 UNION 
							 { ?x a owl:DatatypeProperty }
							 UNION 
							 { ?x a owl:AnnotationProperty }
						} . 
						?x a ?c 
					 FILTER(!isBlank(?x)
					   ) .
					} ORDER BY	?c ?x
				 """)
		return list(qres)
	
		
	def getPropDirectSupers(self, aURI):
		aURI = str(aURI)
		qres = self.rdfgraph.query(
			  """SELECT DISTINCT ?x
				 WHERE {
					 { <%s> rdfs:subPropertyOf ?x }	 
					 FILTER (!isBlank(?x))
				 } ORDER BY ?x	  
				 """ % (aURI))
		return list(qres)	
		
	
	def getPropAllSupers(self, aURI):
		""" 
		note: requires SPARQL 1.1 
		2015-06-04: currenlty not used, inferred from above
		"""
		aURI = str(aURI)
		try:
			qres = self.rdfgraph.query(
				  """SELECT DISTINCT ?x
					 WHERE {
						 { <%s> rdfs:subPropertyOf+ ?x } 
						 FILTER (!isBlank(?x))
					 }	 
					 """ % (aURI))
		except:
			printDebug("... warning: the 'getPropAllSupers' query failed (maybe missing SPARQL 1.1 support?)")
			qres = []
		return list(qres)	


	def getPropAllSubs(self, aURI):
		"""	 
		note: requires SPARQL 1.1	
		2015-06-04: currenlty not used, inferred from above
		"""
		aURI = str(aURI)
		try:
			qres = self.rdfgraph.query(
				  """SELECT DISTINCT ?x
					 WHERE {
						 { ?x rdfs:subPropertyOf+ <%s> } 
						 FILTER (!isBlank(?x))
					 }	 
					 """ % (aURI))
		except:
			printDebug("... warning: the 'getPropAllSubs' query failed (maybe missing SPARQL 1.1 support?)")
			qres = []
		return list(qres)
		
