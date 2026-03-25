.PHONY: push

# kawahara247アカウントでGitHubにプッシュ
push:
	gh auth switch --user kawahara247
	git push --set-upstream origin HEAD
