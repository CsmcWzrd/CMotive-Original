# Classes, Single Inheritance, Constructors, Destructors, New/Delete

This iteration moves the CMotive bootstrap compiler beyond placeholders for the
core object model.

## Implemented behavior

- `Class` declarations lower to concrete C `struct` definitions.
- A root class receives a `CMotiveObject __cmotive_object` header.
- A derived class embeds its validated base class as the first field named
  `__base`, giving the generated C layout an ABI-compatible first-member base
  layout.
- Methods lower to mangled C functions in the form:

  ```c
  ReturnType ClassName__MethodName(ClassName *this, ...);
  ```

- Constructors named as the class lower to `ClassName__ctor` for zero
  parameters and `ClassName__ctor__N` for N parameters.
- Destructors declared as `~ClassName` lower to `ClassName__dtor`.
- Derived constructors call the zero-argument base constructor before field
  initializers and the derived body.
- Derived destructors run the derived body and then call the base destructor.
- `New ClassName(...)` lowers to a generated `ClassName__new[_N](...)` helper.
  That helper calls `CMotive_New(sizeof(ClassName))`, then dispatches the
  matching constructor.
- `Delete objectPointer` lowers to `ClassName__delete(objectPointer)`, which
  dispatches `ClassName__dtor` and then calls `CMotive_Delete`.
- Object method calls such as `obj.Method()` and pointer method calls such as
  `ptr->Method()` lower to their mangled method functions.

## Validation

Semantic analysis now rejects:

- an undefined base class;
- multiple base classes, because this implementation targets CMotive's
  single-inheritance requirement;
- inheritance cycles;
- duplicate methods with the same simple signature;
- constructor/destructor declarations whose names do not match the enclosing
  class.

## Current limits

- Virtual dispatch remains an ABI placeholder; method calls are statically
  lowered.
- Destructor execution during exception unwinding is not complete.
- Constructor overload resolution currently uses argument count rather than full
  type-based overload resolution.
