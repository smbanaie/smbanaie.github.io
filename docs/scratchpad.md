# Admin Panel Rewrite Plan

## Phase 1: Modern Admin Panel Foundation

### 1. Create Modern Base Template
- [x] Create `templates/admin/base.html` with Bootstrap 5
- [x] Add modern CSS styling
- [x] Include all necessary JavaScript libraries
- [x] Add responsive navigation and sidebar

### 2. Update Admin Handler
- [x] Modify `handlers/admin_handler.py` to use new base template
- [x] Update all admin routes to extend base.html
- [x] Ensure proper static file serving

### 3. Create Modern Post Editor
- [x] Create `templates/admin/posts/add.html` with modern UI
- [x] Replace TinyMCE with SimpleMDE (free Markdown editor)
- [x] Add real-time preview functionality
- [x] Implement proper form validation

### 4. Create Post List Page
- [x] Create `templates/admin/posts/list.html` with modern UI
- [x] Add search and filtering functionality
- [x] Implement pagination
- [x] Add edit/delete buttons for each post

### 5. Create Image Upload System
- [x] Create `templates/admin/posts/upload.html` with modern UI
- [x] Add drag-and-drop file upload
- [x] Implement image preview and management
- [x] Add proper file organization by category/date

## Phase 2: Advanced Features

### 6. Add Category Management
- [ ] Create category management interface
- [ ] Add category creation/editing/deletion
- [ ] Implement category hierarchy support

### 7. Add User Management
- [ ] Create user management interface
- [ ] Add user roles and permissions
- [ ] Implement user profile editing

### 8. Add Settings Page
- [ ] Create global settings interface
- [ ] Add site configuration options
- [ ] Implement theme customization

### 9. Add Analytics Dashboard
- [ ] Create dashboard with statistics
- [ ] Add post views and engagement metrics
- [ ] Implement user activity tracking

## Phase 3: Polish and Optimization

### 10. Performance Optimization
- [ ] Optimize CSS and JavaScript loading
- [ ] Implement lazy loading for images
- [ ] Add caching strategies

### 11. Mobile Responsiveness
- [ ] Test and optimize for mobile devices
- [ ] Add touch-friendly interactions
- [ ] Ensure proper responsive behavior

### 12. Accessibility Improvements
- [ ] Add ARIA labels and roles
- [ ] Ensure keyboard navigation
- [ ] Test with screen readers

## Technical Stack

- **Frontend**: Bootstrap 5, SimpleMDE, vanilla JavaScript
- **Backend**: Tornado (Python)
- **Database**: None (file-based content management)
- **Image Storage**: Local filesystem with organized structure

## Key Features

1. **Modern UI**: Clean, responsive design with Bootstrap 5
2. **Markdown Editor**: SimpleMDE for easy content creation
3. **Real-time Preview**: Live preview of Markdown content
4. **Image Management**: Drag-and-drop upload with preview
5. **Post Management**: Easy editing and deletion of posts
6. **Search and Filter**: Quick access to posts by various criteria
7. **Mobile-friendly**: Works well on all screen sizes

## Implementation Notes

- All templates extend `base.html` for consistent styling
- Static files are properly organized in `static/` directory
- JavaScript code is modular and well-commented
- CSS includes custom styles for modern appearance
- All functionality works without external dependencies (except CDN for Bootstrap)

## Current Task Status

**Current Task: Phase 1 - Modern Admin Panel Foundation**
- ✅ Base template created and styled
- ✅ Admin handler updated
- ✅ Post editor created with SimpleMDE
- ✅ Post list page created with modern UI
- ✅ Image upload system created

**Next Phase: Phase 2 - Advanced Features**
- Category Management
- User Management  
- Settings Page
- Analytics Dashboard

The modern admin panel foundation is complete and ready for use. The next phase will add advanced management features.

## Phase 4: Enhanced User/Category Management

### 1. Fix Article Count Display
- [ ] Implement proper article counting for users and categories
- [ ] Replace "در حال محاسبه..." with actual counts
- [ ] Add database/file scanning to count articles by author/category

### 2. Update Userconf Structure
- [ ] Add default user and category fields to userconf.py
- [ ] Add status (active/inactive) for users and categories
- [ ] Update data loading/parsing to handle new fields

### 3. Enhance Category Deletion
- [ ] Add confirmation dialog for category deletion
- [ ] Provide options: keep old category, replace with new, replace with default
- [ ] Implement article migration logic for deleted categories

### 4. Update Add/Edit Forms
- [ ] Add default checkbox/radio for users and categories
- [ ] Add status (active/inactive) selector
- [ ] Update form validation for new fields

### 5. Update List Views
- [ ] Show default status in user/category lists
- [ ] Show active/inactive status with badges
- [ ] Update table columns and styling

### 6. Implement Status Logic
- [x] Prevent deletion of default users/categories with helpful error messages
- [ ] Handle inactive users/categories in article creation
- [x] Add status filtering in lists

### 7. Update Data Persistence
- [ ] Modify _write_userconf_data to handle new fields
- [ ] Ensure backward compatibility with existing data
- [ ] Add validation for default user/category constraints

### 8. Frontend Enhancements
- [ ] Add confirmation dialogs for category deletion with migration options
- [ ] Update JavaScript for new form fields
- [ ] Add visual indicators for default and status fields

## Implementation Order

1. **Task 1**: Fix article count display
2. **Task 2**: Update userconf structure and data handling
3. **Task 3**: Enhance category deletion with migration options
4. **Task 4**: Update forms with default and status fields
5. **Task 5**: Update list views with new columns
6. **Task 6**: Implement status logic and constraints
7. **Task 7**: Update data persistence and validation
8. **Task 8**: Frontend enhancements and polish

## Technical Notes

- Default user/category should be unique (only one can be default)
- Status affects availability in dropdowns and forms
- Category migration requires scanning all articles and updating metadata
- Article count requires scanning content directory for posts
- All changes must maintain backward compatibility

## New Tasks to Complete

### Task 1: Fix Meditation Category Count Issue
- [ ] The Meditation category in category list page has 0 count but it has some articles
- [ ] Investigate why article count is not updating correctly
- [ ] Fix the counting logic for categories

### Task 2: Fix Recalculate Endpoint Error
- [ ] The recalculate endpoint has error
- [ ] Investigate the error and fix it
- [ ] Ensure recalculate functionality works properly

### Task 3: Enforce English Technical Names
- [ ] The technical name for users / categories must be in English
- [ ] If user updates or inserts a new one with non English names, have to be rejected with proper modal message
- [ ] Add validation to reject non-English technical names
- [ ] Display proper error modal when validation fails

### Task 4: Fix User List Page Edit/Delete Buttons
- [ ] The user list page has error - the edit/delete button is not working
- [ ] Nothing shows when clicking on each button
- [ ] Investigate and fix the JavaScript/event handling
- [ ] Ensure edit and delete functionality works properly

### Task 5: Verify Article Saving Location
- [ ] When we add new article, it must saved on the pelican folder in user_area
- [ ] Confirm this happens correctly
- [ ] Check the article saving logic and file paths

### Task 6: Add Pelican Site Generation Feature
- [ ] How to generate the whole pelican content site in admin panel?
- [ ] Add functionality to generate complete Pelican site
- [ ] Create admin panel interface for site generation

### Task 7: Add Comprehensive Tests
- [ ] Add all tests using the provided APIs
- [ ] Create test suite covering all endpoints
- [ ] Ensure proper test coverage for all functionality

### Task 8: Fix Backup Action Error
- [ ] Why backup action in dashboard has error
- [ ] Investigate the backup functionality error
- [ ] Fix the backup action to work properly

### Task 9: Remove All Test Users
- [ ] Remove all test users from the system
- [ ] Clean up test data
- [ ] Ensure no test users remain in userconf.py