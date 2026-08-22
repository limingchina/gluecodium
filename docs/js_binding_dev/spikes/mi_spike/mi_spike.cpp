// Phase 0.2 spike: embind multiple-inheritance mitigation (plan §0.2 / §5.3)
//
// Mirrors functional-tests/functional/input/lime/MultipleInheritance.lime:
//   class MultiClass : OpenClass, NarrowInterface
// Mitigation under test:
//   1. Register exactly ONE primary base via base<> (OpenClass preferred over NarrowInterface).
//   2. Flatten secondary-parent members (NarrowInterface) onto the derived registration.
//   3. Explicit upcast helpers for polymorphic use.
//
// Build: see build.sh. Run: node test.js

#include <emscripten/bind.h>
#include <string>
#include <memory>
#include <iostream>

using namespace emscripten;

// ---- C++ side mirroring what Gluecodium's cpp generator would emit ----

class OpenClass {
public:
    virtual ~OpenClass() = default;
    virtual void parentFunction() {}
    std::string getParentProperty() const { return _parentProperty; }
    void setParentProperty(const std::string& v) { _parentProperty = v; }
private:
    std::string _parentProperty;
};

class NarrowInterface {
public:
    virtual ~NarrowInterface() = default;
    virtual std::string parentFunctionLight() const { return "NarrowInterface"; }
    virtual std::string getParentPropertyLight() const = 0;
};

class MultiClass : public OpenClass, public NarrowInterface {
public:
    void childFunction() {}
    std::string getChildProperty() const { return _childProperty; }
    void setChildProperty(const std::string& v) { _childProperty = v; }
    // NarrowInterface override
    std::string parentFunctionLight() const override { return "MultiClass::parentFunctionLight"; }
    std::string getParentPropertyLight() const override { return "multi-light"; }
private:
    std::string _childProperty;
};

// Factory + explicit upcast helper, as the .lime fixture models them.
static std::shared_ptr<MultiClass> getMultiClass() { return std::make_shared<MultiClass>(); }

// Returns the SAME object viewed through the NarrowInterface base — used to test
// referential equality across the upcast boundary (plan §5.2/§5.3).
static NarrowInterface* upcastToNarrow(MultiClass* instance) {
    return static_cast<NarrowInterface*>(instance);
}

// ---- embind registrations ----

EMSCRIPTEN_BINDINGS(mi_spike) {
    class_<OpenClass>("OpenClass")
        .function("parentFunction", &OpenClass::parentFunction)
        .property("parentProperty", &OpenClass::getParentProperty, &OpenClass::setParentProperty);

    // Secondary parent registered standalone so `upcastToNarrow` results have a JS type.
    class_<NarrowInterface>("NarrowInterface")
        .function("parentFunctionLight", &NarrowInterface::parentFunctionLight)
        .property("parentPropertyLight", &NarrowInterface::getParentPropertyLight);

    // PRIMARY BASE ONLY: OpenClass via base<>; NarrowInterface members are FLATTENED
    // onto MultiClass (bound again against the derived-class member pointers).
    class_<MultiClass, base<OpenClass>>("MultiClass")
        .smart_ptr<std::shared_ptr<MultiClass>>("MultiClass")
        .function("childFunction", &MultiClass::childFunction)
        .property("childProperty", &MultiClass::getChildProperty, &MultiClass::setChildProperty)
        // flattened NarrowInterface members:
        .function("parentFunctionLight", &MultiClass::parentFunctionLight)
        .property("parentPropertyLight", &MultiClass::getParentPropertyLight);

    function("getMultiClass", &getMultiClass);
    function("upcastToNarrow", &upcastToNarrow, allow_raw_pointers());
}
