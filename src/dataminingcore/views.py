from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import numpy as np
import operator
import json
from django.http import HttpResponse

class NaiveBayes(APIView):
    def post(self, request):
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            return Response({"failed":"12"})
        data = pd.read_csv(request.FILES.get('file'))
        if request.POST.get('id_indices'):
            print(json.loads(request.POST.get('id_indices')))
            data=data.drop(json.loads(request.POST.get('id_indices')), axis=1)
        print(data)
    
        column_names=[columnName for (columnName, columnData) in data.iteritems()][:-1]
        last_column_name=[columnName for (columnName, columnData) in data.iteritems()][-1]

        stat_str = request.data['stat']
        stat_dict = json.loads(stat_str)
        stat = pd.DataFrame(stat_dict) 
        print(stat)

        n=dict()
        for uniq in data[last_column_name].unique():
            n[uniq]=data[last_column_name][data[last_column_name] == uniq].count()

        total_stat = data[last_column_name].count()

        P=dict()
        for uniq in data[last_column_name].unique():
            P[uniq]=n[uniq]/total_stat

        n_counts=dict()
        P_array=dict()


        #------------------------For Single Data----------------------------------
        # for uniq in data[last_column_name].unique():
        #     n_counts[uniq]=[]
        #     P_array[uniq]=[]
        # for column_name in column_names:
        #     for uniq in data[last_column_name].unique():
        #         n_counts[uniq].append(data[last_column_name][((data[column_name] == stat[column_name][0]) & (data[last_column_name] == uniq))].count())
        #         P_array[uniq].append(n_counts[uniq][-1]/n[uniq])
        # multiply_array_P=dict()
        # for uniq in data[last_column_name].unique():
        #     multiply_array_P[uniq]=np.prod(P_array[uniq])*P[uniq]
        # won=max(multiply_array_P.items(), key=operator.itemgetter(1))[0]
        # print("X belongs to '"+str(won)+"' class: "+str(multiply_array_P[won])) 
        # return Response({"success":"X belongs to '"+str(won)+"' class: "+str(multiply_array_P[won])}) 

        #------------------------For Multiple Data----------------------------------
        response=dict()
        for i in range(stat.shape[0]):
            for uniq in data[last_column_name].unique():
                n_counts[uniq]=[]
                P_array[uniq]=[]
            for column_name, value in stat.iteritems(): 
                print(column_name,str(value[0])=="Sunny") 
                print(stat.shape[0]) 
                for uniq in data[last_column_name].unique():
                    n_counts[uniq].append(data[last_column_name][((data[column_name] == stat[column_name][i]) & (data[last_column_name] == uniq))].count())
                    P_array[uniq].append(n_counts[uniq][-1]/n[uniq])
            multiply_array_P=dict()
            for uniq in data[last_column_name].unique():
                multiply_array_P[uniq]=np.prod(P_array[uniq])*P[uniq]

            won=max(multiply_array_P.items(), key=operator.itemgetter(1))[0]
            print("X belongs to '"+str(won)+"' class: "+str(multiply_array_P[won])) 
            response["data "+str(i)]="X belongs to '"+str(won)+"' class: "+str(multiply_array_P[won]) 

            # response = HttpResponse(content_type='text/csv')
            # response['Content-Disposition'] = 'attachment; filename=filename.csv'
            # stat.to_csv(path_or_buf=response,sep=',',float_format='%.2f',index=False,decimal=",")
            # return response
        return Response(response) 