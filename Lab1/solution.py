from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Matrix Multiplication Started")
        print("Workers: %d" % len(self.workers))

        matrices = self.read_input()
        mapped = []
        for i in xrange(0, len(self.workers)):
            print("Mapping task to worker %d" % i)
            mapped.append(self.workers[i].mymap(matrices, len(self.workers), i))

        result = self.myreduce(mapped)
        self.write_output(result)

        print("Matrix Multiplication Finished")

    @staticmethod
    @expose
    def mymap(matrices, num_workers, worker_id):
        matrix_a, matrix_b = matrices
        num_rows_a = len(matrix_a)
        rows_per_worker = num_rows_a // num_workers
        start_row = worker_id * rows_per_worker
        end_row = start_row + rows_per_worker if worker_id < num_workers - 1 else num_rows_a

        result = dot_product(matrix_a[start_row:end_row], matrix_b)
        return result

    @staticmethod
    @expose
    def myreduce(mapped):
        print("Reducing results")
        result = []
        for row in mapped:
            result.extend(row.value)
        return result

    def read_input(self):
        matrix_a = []
        matrix_b = []
    
        with open(self.input_file_name, 'r') as file:
    
            for line in file:
                line = line.strip()
                if not line:
                    break
                matrix_a.append([int(x) for x in line.split()])
        
            for line in file:
                matrix_b.append([int(x) for x in line.split()])

        return matrix_a, matrix_b

    def write_output(self, result):
        with open(self.output_file_name, 'w') as file:
            for row in result:
                file.write(' '.join(map(str, row)) + '\n')
        print("Output written to", self.output_file_name)

def dot_product(matrix_a, matrix_b):
    num_rows_a, num_cols_a = len(matrix_a), len(matrix_a[0])
    num_cols_b = len(matrix_b[0])
    result = []
    for i in xrange(num_rows_a):
        row = []
        for j in xrange(num_cols_b):
            cell_value = sum(matrix_a[i][k] * matrix_b[k][j] for k in xrange(num_cols_a))
            row.append(cell_value)
        result.append(row)
    return result