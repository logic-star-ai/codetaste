# Title
Refactor `db.DefaultContext` usage in template-accessible functions

## Summary
Refactor functions used in templates to accept `context.Context` as parameter instead of implicitly using `db.DefaultContext`.

## Why
- Template functions currently call methods that internally use `db.DefaultContext`
- Makes context flow implicit and harder to trace
- Part of broader effort to eliminate implicit default context usage (#27065)

## Changes
**Models - Action/Activity**
- `Action.GetActFullName/GetActUserName/ShortActUserName(...)` → now accept `ctx`
- `Action.GetDisplayName/GetDisplayNameTitle(...)` → now accept `ctx`
- `Action.GetRepo*/ShortRepo*/.../GetRefLink(...)` → now accept `ctx`
- `Action.GetCommentHTMLURL/GetCommentLink/GetIssueTitle(...)` → now accept `ctx`
- `activityQueryCondition(...)` → now accepts `ctx`
- `DeleteOldActions/NotifyWatchersActions(...)` → now accept `ctx`

**Models - Notification**
- `Notification.GetRepo/GetIssue/HTMLURL/Link(...)` → now accept `ctx`
- `GetUIDsAndNotificationCounts(...)` → now accepts `ctx`

**Models - Comment/Issue/Review**
- `Comment.HTMLURL/Link/APIURL/IssueURL/PRURL(...)` → now accept `ctx`
- `Comment.LoadLabel/LoadProject/LoadAssignee*/LoadResolveDoer/LoadDepIssueDetails(...)` → now accept `ctx`
- `Comment.LoadReactions/LoadReview/CodeCommentLink(...)` → now accept `ctx`
- `Comment.Update/UpdateAttachments(...)` → now accept `ctx`
- `CountComments/UpdateComment/InsertIssueComments(...)` → now accept `ctx`
- `Review.HTMLURL/GetCodeCommentsCount(...)` → now accept `ctx`
- `ReviewExists/SubmitReview/MarkReviewsAsStale/MarkConversation/CanMarkConversation/DeleteReview(...)` → now accept `ctx`
- Issue update functions (`UpdateIssueDeadline/UpdateIssueByAPI/ChangeIssueContent/NewIssue...`) → now accept `ctx`

**Models - Project**
- `Project.Link/NumIssues/NumClosedIssues/NumOpenIssues(...)` → now accept `ctx`
- `Board.NumIssues(...)` → now accepts `ctx`
- `NewProject/ChangeProjectStatus*/NewBoard/DeleteBoardByID/SetDefaultBoard/UpdateBoardSorting/MoveIssuesOnProjectBoard(...)` → now accept `ctx`

**Models - Repo**
- `Mirror.GetRepository(...)` → now accepts `ctx`
- `DeleteMirrorByRepoID/MirrorsIterate(...)` → now accept `ctx`
- `IsOwnerMemberCollaborator/CountCollaborators(...)` → now accept `ctx`

**Services/Routers**
- Update all call sites in services/routers to pass context
- Templates updated to pass `ctx` to model methods

## Notes
⚠️ Templates are not statically typed - runtime testing critical
🔍 Breaking change for any external code calling these methods
✅ More explicit context flow, better for tracing/cancellation