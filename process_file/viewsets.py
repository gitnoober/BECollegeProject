from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from process_file.constants import *
from process_file.models import MiscData
from process_file.serializers import MiscDataSerializer
from process_file.service import ProcessFileService


# ViewSets define the view behavior.
class ProcessFileViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs):
        self.service_obj = ProcessFileService()

    def get_serializer_class(self):
        return MiscDataSerializer

    queryset = MiscData.objects.all()

    def list(self, request, *args, **kwargs):
        # qs = MiscData.objects.filter(props__is_fraud__icontains='1')
        qs = MiscData.objects.all()[:5000]
        serialized_data = MiscDataSerializer(qs, many=True).data
        res = {
            'msg': MiscDataConstants.FETCHED_MSG,
            'data': serialized_data
        }
        return Response(res, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        payload = request.data
        file_url = payload.get('file_url')
        n_rows = int(payload.get('n_rows', 1000))
        s_data = self.service_obj.process_file(file_url, n_rows)
        res = {
            "msg": MiscDataConstants.UPLOADED_MSG,
            "data": s_data
        }
        return Response(res, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        data = request.query_params
        is_fraud = data.get('is_fraud')
        cc_num = data.get('cc_num')
        first = data.get('first')
        last = data.get('last')
        gender = data.get('gender')
        city = data.get('city')
        job = data.get('job')
        response = {}
        status_code = 200
        if not pk:
            msg = "Nahi bheja hai pk bhai"
            response['msg'] = msg
            status_code = 400
        else:
            qs = MiscData.objects.filter(parent_id=pk)
            if is_fraud:
                qs = qs.filter(props__is_fraud__icontains='1')
            if cc_num:
                qs = qs.filter(props__cc_num__icontains=cc_num)
            if first:
                qs = qs.filter(props__first__icontains=first)
            if last:
                qs = qs.filter(props__last__icontains=last)
            if gender:
                qs = qs.filter(props__gender__icontains=gender)
            if city:
                qs = qs.filter(props__city__icontains=city)
            if job:
                qs = qs.filter(props__job__icontains=job)
            qs = qs[:5000]
            serialized_data = MiscDataSerializer(qs, many=True).data
            response['msg'] = MiscDataConstants.FETCHED_MSG
            response['data'] = serialized_data

        return Response(response, status_code)
