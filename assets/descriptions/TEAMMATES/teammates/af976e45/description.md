# Standardize modal components across application

## Summary
Replace ~16 individual modal components with a single configurable `SimpleModalComponent` and `SimpleModalService` to ensure consistency and reduce code duplication.

## Why
- Modals have inconsistent colors, styling, and behavior across the application
- Each modal requires separate component, template, and spec files
- High maintenance overhead for similar functionality
- Violates DRY principle

## Changes

### New Components
- `SimpleModalComponent` - configurable modal with 4 types (WARNING, DANGER, INFO, NEUTRAL)
- `SimpleModalService` - service to programmatically open modals
- `SimpleModalType` enum
- Support for HTML content & `TemplateRef` for complex content

### Deleted Components
- `confirm-delete-comment-modal`
- `course-permanent-deletion-confirm-modal`
- `course-soft-deletion-confirm-modal`
- `delete-instructor-confirm-modal`
- `feedback-session-*-modal` (closed, closing-soon, deleted, not-open)
- `regenerate-links-confirm-modal`
- `resend-invitation-email-modal`
- `reset-google-id-confirm-modal`
- `confirm-publishing-session-modal`
- `confirm-unpublishing-session-modal`
- `confirm-session-move-to-recycle-bin-modal`
- `status-message-modal`

### Refactored Components
- `question-edit-form.component`
- `student-profile-page.component`
- `contribution-question-*` components
- `instructor-*` components (home, courses, session-edit, course-enroll, course-student-edit, help-questions)
- `student-list.component`
- `rubric-question-edit-details-form.component`
- `session-edit-form.component`
- `admin-search-page.component`
- ... many more

### API

```typescript
// Confirmation modal (2 buttons)
simpleModalService.openConfirmationModal(
  'Delete student?', 
  SimpleModalType.DANGER, 
  'Are you sure?'
);

// Information modal (1 button)
simpleModalService.openInformationModal(
  'Session closed', 
  SimpleModalType.WARNING, 
  'Content here'
);

// With options
openConfirmationModal(header, type, content, {
  confirmMessage: 'Yes, delete',
  cancelMessage: 'Cancel'
});
```

## Technical Details
- Modal content supports HTML via `[innerHTML]`
- Complex HTML passed as `TemplateRef<any>` for better structure
- Renamed `modalService` → `ngbModal` for clarity
- 4 modal types with distinct styling (colors, icons)
- Consistent button placement and labeling

## Result
- ~500 lines of modal-related code deleted
- Consistent UX across all confirmation/information dialogs
- Easier to maintain and extend
- Better adherence to Material Design principles