from rest_framework import permissions, status, views
from rest_framework.response import Response

from posts.models import Post, Vote
from posts.serializers import VoteSerializer

from a2ausers.models import User


class VoteView(views.APIView):

    def get_permissions(self):
        return (permissions.IsAuthenticated(), )

    # Do, undo upvote/downvote for a post
    def post(self, request, format=None):
        id = request.GET.get('postID')

        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.filter(id=id).first()
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        voter = User.objects.get(id=request.user.id).a2ausers

        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            score = serializer.validated_data.get('score')
            if score == 1:  # upvote / undo upvote
                downvote = Vote.objects.filter(
                    post__id=id, score=-1,
                    user__user__username=request.user.username).first()
                # Need to undo downvote before upvoting
                if downvote is not None:
                    return Response(
                        'You need to undo your downvote before downvoting',
                        status=status.HTTP_400_BAD_REQUEST)

                vote = Vote.objects.filter(
                    post__id=id, score=1,
                    user__user__username=request.user.username).first()

                if vote is None:  # Never upvoted
                    vote = Vote(post=post, user=voter, score=1)
                    vote.save()
                    post.total_vote += 1
                    # post.votes.add(voter)
                    post.save()
                    return Response('Upvote sucessfully.',
                                    status=status.HTTP_201_CREATED)
                else:  # Upvoted => undo upvote
                    # post.votes.remove(voter)
                    post.total_vote -= 1
                    post.save()
                    vote.delete()
                    return Response('Undo upvote sucessfully.',
                                    status=status.HTTP_200_OK)
            else:  # downvote / undo downvote
                upvote = Vote.objects.filter(
                    post__id=id, score=1,
                    user__user__username=request.user.username).first()
                # Need to undo upvote before downvoting
                if upvote is not None:
                    return Response(
                        'You need to undo your upvote before downvoting',
                        status=status.HTTP_400_BAD_REQUEST)

                vote = Vote.objects.filter(
                    post__id=id, score=-1,
                    user__user__username=request.user.username).first()
                if vote is None:  # Never downvoted
                    vote = Vote(post=post, user=voter, score=-1)
                    vote.save()
                    post.total_vote -= 1
                    # post.votes.add(voter)
                    post.save()
                    return Response('Downvote sucessfully.',
                                    status=status.HTTP_201_CREATED)
                else:  # Downvoted => undo downvote
                    # post.votes.remove(voter)
                    post.total_vote += 1
                    post.save()
                    vote.delete()
                    return Response('Undo downvote sucessfully.',
                                    status=status.HTTP_200_OK)

    # Get vote status of the requester on the post
    # Return 1, 0, -1 for upvoted, none, downvoted
    def get(self, request, format=None):
        id = request.GET.get('postID')
        if id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        post = Post.objects.filter(id=id).first()
        if post is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        vote = Vote.objects.filter(
            post__id=id, user__user__username=request.user.username).first()

        if vote is None:
            return Response(0, status=status.HTTP_200_OK)
        else:
            return Response(vote.score, status=status.HTTP_200_OK)
