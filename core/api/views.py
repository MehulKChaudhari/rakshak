from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet

import json

import pickle

protection_level_dict = {
    "KPS": 0.7,
    "MFN": 0.4,
    "ILE": 0,
}


class APIViewSet(ViewSet):

    permission_classes = (IsAuthenticated,)

    def parse_string_social(self, request: Request):

        text = request.data

        global protection_level_dict
        protection_level = protection_level_dict[request.user.protection_level]

        # pass to ML model
        with open(r"ML/Pickle/toxic_vect.pkl", "rb") as f:
            tox = pickle.load(f)

        with open(r"ML/Pickle/severe_toxic_vect.pkl", "rb") as f:
            sev = pickle.load(f)

        with open(r"ML/Pickle/obscene_vect.pkl", "rb") as f:
            obs = pickle.load(f)

        with open(r"ML/Pickle/insult_vect.pkl", "rb") as f:
            ins = pickle.load(f)

        with open(r"ML/Pickle/threat_vect.pkl", "rb") as f:
            thr = pickle.load(f)

        with open(r"ML/Pickle/identity_hate_vect.pkl", "rb") as f:
            ide = pickle.load(f)

        # Load the pickled RDF models
        with open(r"ML/Pickle/toxic_model.pkl", "rb") as f:
            tox_model = pickle.load(f)

        with open(r"ML/Pickle/severe_toxic_model.pkl", "rb") as f:
            sev_model = pickle.load(f)

        with open(r"ML/Pickle/obscene_model.pkl", "rb") as f:
            obs_model = pickle.load(f)

        with open(r"ML/Pickle/insult_model.pkl", "rb") as f:
            ins_model = pickle.load(f)

        with open(r"ML/Pickle/threat_model.pkl", "rb") as f:
            thr_model = pickle.load(f)

        with open(r"ML/Pickle/identity_hate_model.pkl", "rb") as f:
            ide_model = pickle.load(f)

        result = {
            "toxic": False,
            "severe_toxic": False,
            "obscene": False,
            "threat": False,
            "insult": False,
            "identity_hate": False,
        }

        for sentence in text:

            vect = tox.transform([sentence])
            pred_tox = tox_model.predict_proba(vect)[:, 1]

            if pred_tox > protection_level:
                result["toxic"] = True

            vect = sev.transform([sentence])
            pred_sev = sev_model.predict_proba(vect)[:, 1]
            if pred_sev > protection_level + 0.14:
                result["severe_toxic"] = True

            vect = obs.transform([sentence])
            pred_obs = obs_model.predict_proba(vect)[:, 1]
            if pred_obs > protection_level:
                result["obscene"] = True

            vect = thr.transform([sentence])
            pred_thr = thr_model.predict_proba(vect)[:, 1]
            if pred_thr > protection_level:
                result["threat"] = True

            vect = ins.transform([sentence])
            pred_ins = ins_model.predict_proba(vect)[:, 1]
            if pred_ins > protection_level:
                result["insult"] = True

            vect = ide.transform([sentence])
            pred_ide = ide_model.predict_proba(vect)[:, 1]
            if pred_ide > protection_level:
                result["identity_hate"] = True

        return Response(result, status=status.HTTP_200_OK)
