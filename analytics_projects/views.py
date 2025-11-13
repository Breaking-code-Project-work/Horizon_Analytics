from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#here go the import for backend script

class OverviewAPI(APIView):
    """
    API that recieve filters from frontend and give as output a Jason called data
    """
    def post(self, request):
        # Recover filters from Frontend
        filters = request.data.get("filters", {})

        # Pick filters from frontend
        region = filters.get("region")
        macroarea = filters.get("macroarea")

        # variabiles of back end
        numProjects = 1          
        totalFinancing = 1
        numberEndedProjects = 1
        numberNotStartedProjects = 1
        numberProjectsInProgress = 1
        MiddayFinancing = 1
        MiddleNorthFinancing = 1
        numberBigProjects = 1

        Project1 = []
        Project2 = []
        Project3 = []
        Project4 = []
        Project5 = []
        Project6 = []
        Project7 = []
        Project8 = []
        Project9 = []
        Project10 = []

        Sector1 = []
        Sector2 = []
        Sector3 = []
        # Answer JSON
        response_data = {
             "data": {
                "filters": {
                    "region": region,
                    "macroarea": macroarea
                },

                "numProjects": numProjects,    
                "totalFinancing": totalFinancing,  
                "numberEndedProjects": numberEndedProjects,  
                "numberNotStartedProjects": numberNotStartedProjects,  
                "numberProjectsInProgress": numberProjectsInProgress,  
                "MiddayFinancing": MiddayFinancing,  
                "MiddleNorthFinancing": MiddleNorthFinancing,  
                "TopProjects": {  
                    "Project1": Project1,  
                    "Project2": Project2,  
                    "Project3": Project3,  
                    "Project4": Project4,
                    "Project5": Project5,
                    "Project6": Project6,
                    "Project7": Project7,
                    "Project8": Project8,
                    "Project9": Project9,
                    "Project10": Project10
                    },  
                "numberBigProjects": numberBigProjects,  
                "TopSectors": {  
                    "Sector1": Sector1,  
                    "Sector2": Sector2,  
                    "Sector3": Sector3  
                }  
            } 
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
