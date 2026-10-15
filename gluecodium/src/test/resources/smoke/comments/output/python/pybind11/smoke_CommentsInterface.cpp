

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
#include "smoke/CommentsInterface.h"
#include "string"

using CommentsInterface = ::smoke::CommentsInterface;
using SomeStruct = ::smoke::CommentsInterface::SomeStruct;
using SomeEnum = ::smoke::CommentsInterface::SomeEnum;

class CommentsInterfaceTrampoline : public CommentsInterface {
public:
    using CommentsInterface::CommentsInterface;
    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<CommentsInterface> m_impl;

    bool some_method_with_all_comments(
            const ::std::string& input ) override {
        if (m_impl) {
            return m_impl->some_method_with_all_comments(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f6457697468416c6c436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f6457697468416c6c436f6d6d656e7473", some_method_with_all_comments, input);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_with_all_comments, input);
    }
    bool some_method_with_input_comments(
            const ::std::string& input ) override {
        if (m_impl) {
            return m_impl->some_method_with_input_comments(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f6457697468496e707574436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f6457697468496e707574436f6d6d656e7473", some_method_with_input_comments, input);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_with_input_comments, input);
    }
    bool some_method_with_output_comments(
            const ::std::string& input ) override {
        if (m_impl) {
            return m_impl->some_method_with_output_comments(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684f7574707574436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684f7574707574436f6d6d656e7473", some_method_with_output_comments, input);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_with_output_comments, input);
    }
    bool some_method_with_no_comments(
            const ::std::string& input ) override {
        if (m_impl) {
            return m_impl->some_method_with_no_comments(input);
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684e6f436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684e6f436f6d6d656e7473", some_method_with_no_comments, input);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_with_no_comments, input);
    }
    void some_method_without_return_type_with_all_comments(
            const ::std::string& input ) override {
        if (m_impl) {
            m_impl->some_method_without_return_type_with_all_comments(input);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e5479706557697468416c6c436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e5479706557697468416c6c436f6d6d656e7473", some_method_without_return_type_with_all_comments, input);
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, some_method_without_return_type_with_all_comments, input);
    }
    void some_method_without_return_type_with_no_comments(
            const ::std::string& input ) override {
        if (m_impl) {
            m_impl->some_method_without_return_type_with_no_comments(input);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e54797065576974684e6f436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e54797065576974684e6f436f6d6d656e7473", some_method_without_return_type_with_no_comments, input);
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, some_method_without_return_type_with_no_comments, input);
    }
    bool some_method_without_input_parameters_with_all_comments(
            /* no args */ ) override {
        if (m_impl) {
            return m_impl->some_method_without_input_parameters_with_all_comments();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f7574496e707574506172616d657465727357697468416c6c436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f7574496e707574506172616d657465727357697468416c6c436f6d6d656e7473", some_method_without_input_parameters_with_all_comments);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_without_input_parameters_with_all_comments);
    }
    bool some_method_without_input_parameters_with_no_comments(
            /* no args */ ) override {
        if (m_impl) {
            return m_impl->some_method_without_input_parameters_with_no_comments();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f7574496e707574506172616d6574657273576974684e6f436f6d6d656e7473")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f7574496e707574506172616d6574657273576974684e6f436f6d6d656e7473", some_method_without_input_parameters_with_no_comments);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_without_input_parameters_with_no_comments);
    }
    void some_method_with_nothing(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->some_method_with_nothing();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684e6f7468696e67")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974684e6f7468696e67", some_method_with_nothing);
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, some_method_with_nothing);
    }
    void some_method_without_return_type_or_input_parameters(
            /* no args */ ) override {
        if (m_impl) {
            m_impl->some_method_without_return_type_or_input_parameters();
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e547970654f72496e707574506172616d6574657273")) {
        PYBIND11_OVERRIDE_PURE_NAME(void, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e736f6d654d6574686f64576974686f757452657475726e547970654f72496e707574506172616d6574657273", some_method_without_return_type_or_input_parameters);
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, some_method_without_return_type_or_input_parameters);
    }
    bool is_some_property() const override {
        if (m_impl) {
            return m_impl->is_some_property();
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e536f6d6550726f7065727479_get")) {
        PYBIND11_OVERRIDE_PURE_NAME(bool, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e536f6d6550726f7065727479_get", is_some_property);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, is_some_property);
    }
    void set_some_property(const bool value) override {
        if (m_impl) {
            m_impl->set_some_property(value);
            return;
        }
        py::gil_scoped_acquire gil;
        if (py::get_override(static_cast<const CommentsInterface*>(this), "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e536f6d6550726f7065727479_set")) {
            PYBIND11_OVERRIDE_PURE_NAME(void, CommentsInterface, "__gluecodium_callback_736d6f6b652e436f6d6d656e7473496e746572666163652e536f6d6550726f7065727479_set", set_some_property, value);
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, set_some_property, value);
    }
};



void register_smoke_CommentsInterface(py::module_& module) {
auto cls_CommentsInterface = py::class_<CommentsInterface, std::shared_ptr<CommentsInterface>, CommentsInterfaceTrampoline>(module, "smoke_CommentsInterface")
        .def("__gluecodium_id__", [](const CommentsInterface& self) {
            return gluecodium::python::native_identity(self);
        })
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<CommentsInterface> native) {
            auto self = std::make_shared<CommentsInterfaceTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def("some_method_with_all_comments", [](CommentsInterface& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_with_all_comments(input); });
        }, py::arg("input"))
        .def("some_method_with_input_comments", [](CommentsInterface& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_with_input_comments(input); });
        }, py::arg("input"))
        .def("some_method_with_output_comments", [](CommentsInterface& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_with_output_comments(input); });
        }, py::arg("input"))
        .def("some_method_with_no_comments", [](CommentsInterface& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_with_no_comments(input); });
        }, py::arg("input"))
        .def("some_method_without_return_type_with_all_comments", [](CommentsInterface& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_without_return_type_with_all_comments(input); });
        }, py::arg("input"))
        .def("some_method_without_return_type_with_no_comments", [](CommentsInterface& self, const ::std::string& input) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_without_return_type_with_no_comments(input); });
        }, py::arg("input"))
        .def("some_method_without_input_parameters_with_all_comments", [](CommentsInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_without_input_parameters_with_all_comments(); });
        })
        .def("some_method_without_input_parameters_with_no_comments", [](CommentsInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_without_input_parameters_with_no_comments(); });
        })
        .def("some_method_with_nothing", [](CommentsInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_with_nothing(); });
        })
        .def("some_method_without_return_type_or_input_parameters", [](CommentsInterface& self) {
            return gluecodium::python::call_native([&]() -> decltype(auto) { return self.some_method_without_return_type_or_input_parameters(); });
        })
        .def_property("is_some_property", [](const CommentsInterface& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.is_some_property();
            });
        }, [](CommentsInterface& self, const bool value) {
            gluecodium::python::call_native([&] {
                self.set_some_property(value);
            });
        })
        ;

auto cls_CommentsInterfaceSomeStruct = py::class_<SomeStruct>(cls_CommentsInterface, "SomeStruct")
        .def_property("some_field", [](const SomeStruct& self) -> decltype(auto) {
            return
                (self.some_field)
            ;
        }, [](SomeStruct& self, const bool value) {

                self.some_field = value;

        })
        .def(py::init<>())
        .def(py::init<bool>(), py::arg("some_field"))
        ;

auto cls_CommentsInterfaceSomeEnum = py::enum_<SomeEnum>(cls_CommentsInterface, "SomeEnum")
        .value("USELESS", SomeEnum::USELESS)
        .value("USEFUL", SomeEnum::USEFUL)
        ;


}
