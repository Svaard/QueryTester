from rdflib import Graph
import csv

class SPARQLQuery:

	def __init__(self):
		self.directory = r'test.ttl'
		self.graph = Graph()
		self.parse_graph(self.graph)
		# results = self.run_query(self.graph)
		# self.write_results(results)

	def parse_graph(self, graph):
		print('Loading rdf model')
		'''Initialize graph file that we will load our rdf model into'''
		graph.parse(self.directory)

	def run_query(self, graph, user_query):
		query = user_query
		print('Running query: ', query)
		'''Store the result of our query into result variable'''
		result = graph.query(query)
		print('Number of results: ', len(result))
		for row in result:
			print(f'Title: {row.title or "":<20} price: {row.price:<10}', end='\n')
		return result

	def write_results(self, filename, result):
		'''Write our results to a .csv file'''
		with open(filename + '.csv' if not filename.endswith('.csv') else filename, 'w', newline='') as csvfile:
			querywriter = csv.writer(csvfile)
			querywriter.writerow(['Title', 'Price'])
			for row in result:
				querywriter.writerow([row.title, row.price])