from CREPE import CREPE, CrepeModus, get_queue, QueueService, NeuroProcessor

import time
import os,sys,inspect 
# Find the path to the test_data folder.
__currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
path_to_test_data_folder = __currentdir + "/test_data/"

def main():
#    queue_services = []

#    neuro_processor_kwargs = {"meame_address":"127.0.0.1", "meame_port":40000,"bitrate":1000}    
#    queue_services.append([NeuroProcessor, neuro_processor_kwargs])


    crep = CREPE(modus=CrepeModus.OFFLINE)#, queue_services=queue_services)

    #readout_queue = get_queue(crep, "NEUROPROCESSOR")
    end = QueueService(name="END", queue_in=crep.get_last_queue())
    while True:
        data = end.get()
        print("Got: ", data)
        if data is False:
            print("shutting down crepe")
            crep.shutdown()
            return

if __name__ == "__main__":
    main()
