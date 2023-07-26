git branch | while read branch; do
    git checkout $branch
    git filter-branch --tree-filter 'find . -name "*.jpg" -o -name "*.png" -o -name "*.pth" -exec rm -f {} \;' HEAD
    git reflog expire --expire=now --all && git gc --prune=now --aggressive
done
