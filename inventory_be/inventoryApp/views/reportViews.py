from django.conf                                      import settings
from django.db.models.query import EmptyQuerySet
from django.http                                      import request
from rest_framework                                   import generics, status
from rest_framework.response                          import Response
from rest_framework.permissions                       import IsAuthenticated
from rest_framework_simplejwt.backends                import TokenBackend
from inventoryApp.models.report                 import Report
from inventoryApp.serializers.reportSerializer   import ReportSerializer
import datetime
from django.utils import timezone


class ReportCreateView(generics.CreateAPIView):
    queryset           = Report.objects.all()
    serializer_class   = ReportSerializer
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        token        = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        print(timezone.now())
        ReportStatus = request.data['status']
        itemId = request.data['item']
        lastReport = (Report.objects.filter(item_id=itemId)).last()
        if(lastReport):
            lastReportStatus = lastReport.status
            lastReportEmployee = lastReport.employee

            if(lastReportStatus == ReportStatus):
                stringResponse = {'detail':'duplicated'}
                return Response(stringResponse, status=status.HTTP_208_ALREADY_REPORTED)

            if(ReportStatus == 'input'):
                request.data['employee'] = lastReportEmployee
        
        if (lastReport == None  and ReportStatus == 'input'):
                stringResponse = {'detail':'without output'}
                return Response(stringResponse, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ReportDetailView(generics.RetrieveAPIView):
    queryset           = Report.objects.all()
    serializer_class   = ReportSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get_object()

class ReportListView(generics.ListAPIView):
    serializer_class   = ReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = Report.objects.all()
        return queryset.order_by('-id')


class ReportOutputListView(generics.ListAPIView):
    serializer_class   = ReportSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        token        = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data   = tokenBackend.decode(token,verify=False)
        
        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = Report.objects.all().order_by('-id')
        inputs = Report.objects.filter(status='input')
        outputs = Report.objects.filter(status='output')
        return (filterOutputs(queryset,inputs,outputs))


class ReportUpdateView(generics.UpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        token = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != self.kwargs['user']:
            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().get_object()

    def put(self, request, *args, **kwargs):
        token = self.request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != self.kwargs['user']:

            archivo = request.data['firma_url']
            archivo.name = 'firma.png'
            request.data['firma_url'] = archivo

            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        return super().put(request, *args, **kwargs)

class ReportDeleteView(generics.DestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token, verify=False)

        if valid_data['user_id'] != kwargs['user']:
            stringResponse = {'detail': 'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        try:
            reportD = Report.objects.filter(id=kwargs['pk'])
            reportD.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Report.DoesNotExist:
            stringResponse = {'detail': 'reporte no existe'}
            return Response(stringResponse, status=status.HTTP_404_NOT_FOUND)   





# function para filtrar los reportes

def filterOutputs (reports,inputsList,outputsList):
  inputs = inputsList
  outputs = outputsList
  finalList = []
  def quantityOutputsByItem(itemId):
    outputsSize = [i for i in outputs if str(i).split(" ")[1] == itemId]
    return (len(outputsSize))

  def quantityInputsByItem(itemId):
    inputSize = [i for i in inputs if str(i).split(" ")[1] == itemId]
    return (len(inputSize))


  for report in reports:
    if ( quantityOutputsByItem(str(report).split(" ")[1]) != quantityInputsByItem(str(report).split(" ")[1])):
        if (len([i for i in finalList if str(i).split(" ")[1] == str(report).split(" ")[1]]) == 0):
            finalList.append(report)
        


  return finalList