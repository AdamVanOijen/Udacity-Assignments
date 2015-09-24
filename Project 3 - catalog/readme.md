before running this application make sure that the 'flask', 'sqlalchemy' and 'oauth2' modules are installed on your machine.

To run this application, change directory in to 'catalog', and run python project.py.

Using The Application...

When the user visits the homepage ( '/' ), they will see 'Latest Items' and 'Categories' sections. Clicking on any of the items under 'Latest Items' will
redirect them to the item's corresponding 'Categories' page ( '/categories/id/<int:id>' ) which contains all items related to the category; clicking on any
of the items under the 'Categories' section will also redirect the user to ( '/categories/id/<int:id>' ). There is also a 'login' button located at the top of the page that 
redirects the user to a page where they can log in to their google+ account ( '/login' ). 

After successfully logging in, the user is redirected to the homepage, except there will be an 'add category' button located at the bottom of the page and 'edit category' 
buttons next to the categories they created.

Clicking on 'add category' will redirect the user to '/categories/new' where they can create a new category. After submitting a name for their new category, they will be 
redirected to the homepage. 
The user can then continue to click on 'edit category' next to their newly created category which will redirect them to /categories/id/<int:id>/edit-- to add items, edit items, delete items or delete the whole category itself.

To delete a category click 'delete category' at the bottom of '/categories/id/<int:id>/edit' page -- clicking it will redirect the user to a confirmation page
at /categories/id/<int:id>/delete.

note: i added some categories / items of my own (under my own google+ signin) to the database 
to demonstrate that the user can only edit their own categories.
