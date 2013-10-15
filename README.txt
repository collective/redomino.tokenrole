redomino.tokenrole
==================

This product allows you to share roles about a specific Plone content to an 
unregistered user through a link.

TokenRole use borg.localrole to assign localroles in context.

PAS Plugin which can assign localroles on a context to anonymous 
users providing a specific token is provided.

After you install redomino.tokenrole through Plone Control Panel, go to
any Plone Page and activate TokenRole support using the specific
action in the content actions menu.

A new content tab will appear to let you manage your tokens on that
page: create a new one leaving there what the system suggests or
modifying it as you need (Manager or Site Administrator role is required). Now try to access the provided url with
an unpriviledged user and you'll get the role you granted on that context.

You can manage the token role (edit, delete, modify or distribute via mail).

.. figure:: https://github.com/redomino/redomino.tokenrole/raw/master/docs/resources/add_token.png
   :align: center

   Token role creation


The default policy which comes with redomino.tokenrole implement this annotating
information on the context, managed through a browser view.

.. figure:: https://github.com/redomino/redomino.tokenrole/raw/master/docs/resources/manage_tokens.png
   :align: center

   Tokens management interface

Usage
-----

* Install the redomino.tokenrole plugin through the quick installer

Credits
-------

Incredibly easy was to have this work done starting out from AutoRole 
product and its PAS plugin, and of course many thanks to borg.localrole
for the incredibly easy way of providing localroles on context.

Thanks to Fabrizio Reale, Redomino and ITCILO for inspiring and sponsoring this
effort.
  
First implemented by Maurizio Delmonte.

