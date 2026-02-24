import os

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class OneInchQuoteView(APIView):
    def get(self, request):
        api_key = os.environ.get("ONEINCH_API_KEY")
        if not api_key:
            return Response({"detail": "ONEINCH_API_KEY is not configured"}, status=status.HTTP_501_NOT_IMPLEMENTED)

        chain_id = int(request.query_params.get("chainId", "137"))
        src = request.query_params.get("src")
        dst = request.query_params.get("dst")
        amount = request.query_params.get("amount")

        if not src or not dst or not amount:
            return Response({"detail": "Missing required params: src, dst, amount"}, status=status.HTTP_400_BAD_REQUEST)

        base = os.environ.get("ONEINCH_BASE_URL", "https://api.1inch.com/swap/v6.1").rstrip("/")
        url = f"{base}/{chain_id}/quote"
        headers = {"Authorization": f"Bearer {api_key}"}
        resp = requests.get(url, params={"src": src, "dst": dst, "amount": amount}, headers=headers, timeout=20)
        return Response(resp.json(), status=resp.status_code)


class OneInchSwapTxView(APIView):
    """
    Returns tx calldata for Classic Swap API (wallet should sign/broadcast client-side).
    """

    def get(self, request):
        api_key = os.environ.get("ONEINCH_API_KEY")
        if not api_key:
            return Response({"detail": "ONEINCH_API_KEY is not configured"}, status=status.HTTP_501_NOT_IMPLEMENTED)

        chain_id = int(request.query_params.get("chainId", "137"))
        src = request.query_params.get("src")
        dst = request.query_params.get("dst")
        amount = request.query_params.get("amount")
        from_address = request.query_params.get("fromAddress")
        slippage = request.query_params.get("slippage", "1")

        if not src or not dst or not amount or not from_address:
            return Response(
                {"detail": "Missing required params: src, dst, amount, fromAddress"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base = os.environ.get("ONEINCH_BASE_URL", "https://api.1inch.com/swap/v6.1").rstrip("/")
        url = f"{base}/{chain_id}/swap"
        headers = {"Authorization": f"Bearer {api_key}"}

        params = {
            "src": src,
            "dst": dst,
            "amount": amount,
            "fromAddress": from_address,
            "slippage": slippage,
        }

        referrer = os.environ.get("ONEINCH_REFERRER_ADDRESS")
        fee = os.environ.get("ONEINCH_FEE")  # Classic Swap API expects a percent string, e.g. "1"
        if referrer:
            params["referrerAddress"] = referrer
        if fee:
            params["fee"] = fee

        resp = requests.get(url, params=params, headers=headers, timeout=30)
        return Response(resp.json(), status=resp.status_code)

