# Setting up a PBNI Extension
---

## Extension Template
It is easiest to use [this github template](https://github.com/informaticon/div.cpp.base.pbni-extension-template).
After creating the new repo follow the steps in the Readme to finish setting it up.

## Structure
For every User Object you want to add to PowerBuilder, create a `.cpp` file and a `.h` file with one Class inside them.
The Class has methods that will be exported and usable in PowerBuilder.
The C++ methods take in special types as arguments which are mapped to the PowerBuilder Types.

See [the docs](./variables.md).


### Header
Inside the header file, create your Class and extend Inf::PBNI_Class. Then you can add all your Method Declarations. The Argument and Return Types of your Methods should all be `Inf::PB<type>` or `void`.

```cpp
// MyExtensionClass.h
class MyExtensionClass : public Inf::PBNI_Class
{
	// Put your methods here
	void Example(Inf::PBInt some_number);
}
```

### Source
Inside the Source File call `INF_REGISTER_CLASS` once. Then define your Methods and register each using `INF_REGISTER_FUNC`.
```cpp
// MyExtensionClass.cpp
#include "MyExtensionClass.h"

#include <WinUser.h>

// This will be the Name of the PowerBuilder user object.
INF_REGISTER_CLASS(MyExtensionClass, L"u_my_extension_class");

// The second argument is the name used by PowerBuilder, after the 2nd argument, the argument names follow.
INF_REGISTER_FUNC(Example, L"of_example", L"ai_some_number");
void MyExtensionClass::Example(Inf::PBInt some_number)
{
	MessageBoxW(NULL, L"This is an example", L"Message", MB_OK);
}
```

Make sure to never use the `INF_REGISTER_[...]` functions inside a Header File, this way the header file could be included into multiple Source Files and gets run multiple times.  
Also make sure to register the Class before you register the Methods.
