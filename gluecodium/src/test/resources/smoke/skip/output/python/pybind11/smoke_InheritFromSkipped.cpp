

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InheritFromSkipped.h"
#include "smoke/SkipProxy.h"
#include "smoke/SkippedEverywhere.h"
#include "smoke/SkippedEverywhereEnum.h"
#include "string"

using InheritFromSkipped = ::smoke::InheritFromSkipped;

class InheritFromSkippedTrampoline : public InheritFromSkipped {
public:
    using InheritFromSkipped::InheritFromSkipped;
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<InheritFromSkipped> m_impl;

    ::std::string not_in_java(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_java(input);
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4a617661")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4a617661", not_in_java, input);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InheritFromSkipped, not_in_java, input);
    }
    bool not_in_swift(
            const bool input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_swift(input);
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e5377696674")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e5377696674", not_in_swift, input);
        }
        PYBIND11_OVERRIDE_PURE(bool, InheritFromSkipped, not_in_swift, input);
    }
    float not_in_dart(
            const float input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_dart(input);
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e44617274")) {
        PYBIND11_OVERRIDE_PURE_NAME(float, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e44617274", not_in_dart, input);
        }
        PYBIND11_OVERRIDE_PURE(float, InheritFromSkipped, not_in_dart, input);
    }
    float not_in_kotlin(
            const float input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->not_in_kotlin(input);
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4b6f746c696e")) {
        PYBIND11_OVERRIDE_PURE_NAME(float, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e6e6f74496e4b6f746c696e", not_in_kotlin, input);
        }
        PYBIND11_OVERRIDE_PURE(float, InheritFromSkipped, not_in_kotlin, input);
    }
    ::std::string get_skipped_in_java() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_in_java();
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::std::string, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_get", get_skipped_in_java);
        }
        PYBIND11_OVERRIDE_PURE(::std::string, InheritFromSkipped, get_skipped_in_java);
    }
    void set_skipped_in_java(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_in_java(value);
            return;
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4a617661_set", set_skipped_in_java, value);
        }
        PYBIND11_OVERRIDE_PURE(void, InheritFromSkipped, set_skipped_in_java, value);
    }
    bool is_skipped_in_swift() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->is_skipped_in_swift();
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_get", is_skipped_in_swift);
        }
        PYBIND11_OVERRIDE_PURE(bool, InheritFromSkipped, is_skipped_in_swift);
    }
    void set_skipped_in_swift(const bool value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_in_swift(value);
            return;
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e5377696674_set", set_skipped_in_swift, value);
        }
        PYBIND11_OVERRIDE_PURE(void, InheritFromSkipped, set_skipped_in_swift, value);
    }
    float get_skipped_in_dart() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_in_dart();
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(float, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_get", get_skipped_in_dart);
        }
        PYBIND11_OVERRIDE_PURE(float, InheritFromSkipped, get_skipped_in_dart);
    }
    void set_skipped_in_dart(const float value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_in_dart(value);
            return;
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e44617274_set", set_skipped_in_dart, value);
        }
        PYBIND11_OVERRIDE_PURE(void, InheritFromSkipped, set_skipped_in_dart, value);
    }
    float get_skipped_in_kotlin() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_in_kotlin();
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(float, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_get", get_skipped_in_kotlin);
        }
        PYBIND11_OVERRIDE_PURE(float, InheritFromSkipped, get_skipped_in_kotlin);
    }
    void set_skipped_in_kotlin(const float value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_in_kotlin(value);
            return;
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b6970706564496e4b6f746c696e_set", set_skipped_in_kotlin, value);
        }
        PYBIND11_OVERRIDE_PURE(void, InheritFromSkipped, set_skipped_in_kotlin, value);
    }
    ::smoke::SkippedEverywhere get_skipped_everywhere() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_everywhere();
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::smoke::SkippedEverywhere, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265_get", get_skipped_everywhere);
        }
        PYBIND11_OVERRIDE_PURE(::smoke::SkippedEverywhere, InheritFromSkipped, get_skipped_everywhere);
    }
    void set_skipped_everywhere(const ::smoke::SkippedEverywhere& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_everywhere(value);
            return;
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265_set", set_skipped_everywhere, value);
        }
        PYBIND11_OVERRIDE_PURE(void, InheritFromSkipped, set_skipped_everywhere, value);
    }
    ::smoke::SkippedEverywhereEnum get_skipped_everywhere_too() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_skipped_everywhere_too();
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265546f6f_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(::smoke::SkippedEverywhereEnum, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265546f6f_get", get_skipped_everywhere_too);
        }
        PYBIND11_OVERRIDE_PURE(::smoke::SkippedEverywhereEnum, InheritFromSkipped, get_skipped_everywhere_too);
    }
    void set_skipped_everywhere_too(const ::smoke::SkippedEverywhereEnum value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_skipped_everywhere_too(value);
            return;
        }
        if (py::get_override(static_cast<const InheritFromSkipped*>(this), "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265546f6f_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, InheritFromSkipped, "__gluecodium_callback_736d6f6b652e536b697050726f78792e736b697070656445766572797768657265546f6f_set", set_skipped_everywhere_too, value);
        }
        PYBIND11_OVERRIDE_PURE(void, InheritFromSkipped, set_skipped_everywhere_too, value);
    }
};



void register_smoke_InheritFromSkipped(py::module_& module) {
auto cls_InheritFromSkipped = py::class_<InheritFromSkipped, ::smoke::SkipProxy, std::shared_ptr<InheritFromSkipped>, InheritFromSkippedTrampoline>(module, "smoke_InheritFromSkipped")
        .def("__gluecodium_id__", [](const InheritFromSkipped& self) {
            return gluecodium::python::native_identity(self);
        })
        .def_static("__gluecodium_downcast__", [](const py::object& native) -> py::object {
            try {
                auto base = native.cast<std::shared_ptr<::smoke::SkipProxy>>();
                auto derived = gluecodium::python::dynamic_pointer_cast<InheritFromSkipped>(base);
                if (derived) return py::cast(derived);
            } catch (const py::cast_error&) {
            }
            return py::none();
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<InheritFromSkipped> native) {
            auto self = std::make_shared<InheritFromSkippedTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("not_in_java", [](InheritFromSkipped& self, const ::std::string& input) {
            return self.not_in_java(input);
        }, py::arg("input"))
        .def("not_in_swift", [](InheritFromSkipped& self, const bool input) {
            return self.not_in_swift(input);
        }, py::arg("input"))
        .def("not_in_dart", [](InheritFromSkipped& self, const float input) {
            return self.not_in_dart(input);
        }, py::arg("input"))
        .def("not_in_kotlin", [](InheritFromSkipped& self, const float input) {
            return self.not_in_kotlin(input);
        }, py::arg("input"))
        .def_property("skipped_in_java", [](const InheritFromSkipped& self) {
            return self.get_skipped_in_java();
        }, [](InheritFromSkipped& self, const ::std::string& value) {
            self.set_skipped_in_java(value);
        })
        .def_property("is_skipped_in_swift", [](const InheritFromSkipped& self) {
            return self.is_skipped_in_swift();
        }, [](InheritFromSkipped& self, const bool value) {
            self.set_skipped_in_swift(value);
        })
        .def_property("skipped_in_dart", [](const InheritFromSkipped& self) {
            return self.get_skipped_in_dart();
        }, [](InheritFromSkipped& self, const float value) {
            self.set_skipped_in_dart(value);
        })
        .def_property("skipped_in_kotlin", [](const InheritFromSkipped& self) {
            return self.get_skipped_in_kotlin();
        }, [](InheritFromSkipped& self, const float value) {
            self.set_skipped_in_kotlin(value);
        })
        ;


}
