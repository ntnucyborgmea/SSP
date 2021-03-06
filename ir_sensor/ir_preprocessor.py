import json
from CREPE.communication.queue_service import QueueService


# TODO: Input validation and error messages

# IR sensor preprocessor 
# Takes JSON sensor data from the hardware-api, preprocesses, sends to meame
# Due to the unfortunate lack of healthy cell cultures, this performs
# all stages of the analysis, and essentially attempts to send the conclusion
# through the nevral network. 
# In more "proper" circumstances, this would perform simple operations
# on the data, such as Fourier transforms.

class IRPreprocessor(QueueService):

    def __init__(self, queue_out, queue_in, name="IRPrePros"):
        # Initialize queue service
        QueueService.__init__(
            self, 
            name=name, 
            queue_out=queue_out, 
            queue_in=queue_in
        )
        
        # Set a threshold for whether or not a pixel is part of hand or not.
        self.on_threshold = 128   

        # Set some thresholds for how many pixels a rock, scissors and paper
        # have.
        self.rock_threshold = 20  # TODO: Placeholder
        self.scissors_threshold = 28 #TODO: Placeholder
        self.paper_threshold = 36  # TODO: placeholder
        

    def run(self):
        while True:
            # Fetch new json item to process
            new_datai_j = self.get()
            new_data = json.loads(new_data_j)
            # Try to get data from it
            conclusion = self.analyze_simple(new_data)
            # Send processed data to meame
            self.meame_encoder(conclusion)
    
            
    def analyze_simple(self, ir_mat):
        '''
        Perform a simple analysis of the matrix, by counting the number of
        "on" pixels. It is assumed that different shapes will have different
        numbers of "on" pixels. For example: Rock < scissors < paper. 
        :param byte[] ir_mat: NxM IR data matrix
        Returns one of 4 conclusions: "None", "Rock", "Scissors" or "Paper"
        '''
        mat_N = len(ir_mat)  # Number of rows
        mat_M = len(ir_mat[0])  # Number of columns
        on_count = 0
        for i in range(0, mat_N):
            for j in range(0, mat_M):
                if ir_mat[i][j] > self.on_threshold: 
                    on_count += 1
        if on_count < self.rock_threshold:
            return "None"
        elif on_count < self.scissors_threshold:
            return "Rock"
        elif on_count < self.paper_threshold: 
            return "Scissors"
        else:
            return "Paper"
        

    def meame_encoder(self, guess):
        ''' 
        Translates the preprocessed data, in this case the system's current
        guess, into a set of stimuli instructions and transmits them to 
        MEAME
        :param str guess: A string, either "None", "Rock", "Paper", or 
        "Scissors".
        Returns status of transmission
        '''
        pass 


def main():
    pass

if __name__ == '__main__':
    main()
