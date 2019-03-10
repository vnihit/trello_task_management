from django.shortcuts import render
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from .models import Boards, Lists, Cards
from .serializers import BoardsSerializer, ListSerializer, CardSerializer


# Create your views here.
@api_view(["POST"])
def CreateBoard(request):
    """
    Create new board for current user.
    """
    user = request.user
    labels = request.data.get("labels")
    if len(labels) > 6:
        return Response(
            {"message": "Maximum 6 labels are allowed."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    board_data = {"owner": user.id, "name": request.data.get("name"), "labels": labels}
    serializer = BoardsSerializer(data=board_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def ListBoards(request):
    """
    List all boards belonging to the current user.
    """
    user = request.user
    boards = Boards.objects.filter(owner=user)
    serializer = BoardsSerializer(boards, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def RenameBoard(request, pk):
    """
    Rename a board.
    """
    user = request.user
    try:
        board = Boards.objects.get(id=pk)
    except:
        raise Http404

    if board.owner != user:  # only update board owned by the user
        return Response(
            {"message": "You are not authorized to rename this board."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    new_name = request.data.get("name")
    serializer = BoardsSerializer(board, data={"name": new_name}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def BoardStatusUpdate(request, pk):
    """
    Change the status (active/archive) of a board with id=pk.
    """
    user = request.user
    try:
        board = Boards.objects.get(id=pk)
    except:
        raise Http404

    if board.owner != user:  # only update board owned by the user
        return Response(
            {"message": "You are not authorized to alter this board."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    new_status = request.data.get("status")
    serializer = BoardsSerializer(board, data={"status": new_status}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def CreateList(request, pk):
    """
    Create list for board with id=pk.
    """
    user = request.user
    try:
        board = Boards.objects.get(id=pk)
    except:
        raise Http404

    if board.owner != user:  # create lists only in a board owned by the user
        return Response(
            {"message": "You are not authorized to create lists for this board"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    list_data = {"name": request.data.get("name"), "board": board.id, "card_order": []}
    serializer = ListSerializer(data=list_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def RenameList(request, pk):
    """
    Rename a list with id=pk.
    """
    user = request.user
    try:
        user_list = Lists.objects.get(id=pk)
    except:
        raise Http404

    if user_list.board.owner != user:  # only update lists owned by the user
        return Response(
            {"message": "You are not authorized to alter this list."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    new_name = request.data.get("name")
    serializer = ListSerializer(user_list, data={"name": new_name}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def ListStatusUpdate(request, pk):
    """
    Change the status (active/archive) of a list with id=pk.
    """
    user = request.user
    try:
        user_list = Lists.objects.get(id=pk)
    except:
        raise Http404

    if user_list.board.owner != user:  # only update list owned by the user
        return Response(
            {"message": "You are not authorized to alter this list."},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    new_status = request.data.get("status")
    serializer = ListSerializer(user_list, data={"status": new_status}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_lists(request, pk):
    """
    Get all lists belonging to a board with id=pk.
    """
    user = request.user
    try:
        board = Boards.objects.get(id=pk)
    except:
        raise Http404

    if board.owner != user:  # get lists only in a board owned by the user
        return Response(
            {"message": "You are not authorized to access lists for this board"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    lists = Lists.objects.filter(board=board)
    serializer = ListSerializer(lists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def CreateCards(request, pk):
    """
    Create card for a given list with id=pk.
    """
    user = request.user
    try:
        card_list = Lists.objects.get(id=pk)
    except:
        raise Http404

    if card_list.board.owner != user:  # only create card in lists owned by the user
        return Response(
            {"message": "You are not authorized to create a card in this list."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    data = request.data
    card_data = {"list_instance": card_list.id, **data}

    serializer = CardSerializer(data=card_data)
    if serializer.is_valid():
        serializer.save()
        card_list.card_order.append(serializer.data["id"])
        card_list.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def ChangeCardOrder(request, pk):
    """
    Input: current index of a card with id=pk, new index of the card
    output: Changes the order of card id in list.card_
    """
    user = request.user
    data = request.data
    new_index = data.get("new_index") #new position at which we want to move the card
    card = Cards.objects.get(id=pk)
    old_index = card.list_instance.card_order.index(card.id) # previous position of the card
    list_instance = card.list_instance
    list_instance.card_order.insert(new_index, list_instance.card_order.pop(old_index)) # change the location of the card on the list card_order
    list_instance.save()
    return Response({"message": "Order changed."}, status=status.HTTP_200_OK)    


@api_view(["PATCH"])
def ChangeCardList(request):
    """
    Move a card from one list to another.
    """
    user = request.user
    data = request.data
    try:
        new_list = Lists.objects.get(id=data.get("list_instance"))
    except:
        raise Http404

    if new_list.board.owner != user:
        return Response(
            {"message": "You are not authorized to access this list."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    card = Cards.objects.get(id=data.get("card_id"))
    old_list = card.list_instance
    
    if card.list.board != new_list.board:
        return Response(
            {"message": "The selected list does not belong to this board."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    new_card_data = {"list_instance": new_list.id}

    serializer = CardSerializer(card, data=new_card_data, partial=True)

    if serializer.is_valid():
        serializer.save()
        old_list.card_order.remove(card.id) # remove the card from order list of the previous list
        old_list.save()
        new_list.card_order.append(card.id) # add the card to the order list of the new list
        new_list.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

