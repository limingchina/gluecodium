

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/CommentsInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using CommentsInterface = ::smoke::CommentsInterface;

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
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->some_method_with_all_comments(input);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_with_all_comments, input);
    }
    bool some_method_with_input_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->some_method_with_input_comments(input);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_with_input_comments, input);
    }
    bool some_method_with_output_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->some_method_with_output_comments(input);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_with_output_comments, input);
    }
    bool some_method_with_no_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->some_method_with_no_comments(input);
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_with_no_comments, input);
    }
    void some_method_without_return_type_with_all_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->some_method_without_return_type_with_all_comments(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, some_method_without_return_type_with_all_comments, input);
    }
    void some_method_without_return_type_with_no_comments(
            const ::std::string& input ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->some_method_without_return_type_with_no_comments(input);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, some_method_without_return_type_with_no_comments, input);
    }
    bool some_method_without_input_parameters_with_all_comments(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->some_method_without_input_parameters_with_all_comments();
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_without_input_parameters_with_all_comments);
    }
    bool some_method_without_input_parameters_with_no_comments(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->some_method_without_input_parameters_with_no_comments();
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, some_method_without_input_parameters_with_no_comments);
    }
    void some_method_with_nothing(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->some_method_with_nothing();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, some_method_with_nothing);
    }
    void some_method_without_return_type_or_input_parameters(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->some_method_without_return_type_or_input_parameters();
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, some_method_without_return_type_or_input_parameters);
    }
    bool is_some_property() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->is_some_property();
        }
        PYBIND11_OVERRIDE_PURE(bool, CommentsInterface, is_some_property);
    }
    void set_some_property(const bool value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_some_property(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, CommentsInterface, set_some_property, value);
    }
};

void register_smoke_CommentsInterface(py::module_& module) {
    py::class_<CommentsInterface, std::shared_ptr<CommentsInterface>, CommentsInterfaceTrampoline>(module, "smoke_CommentsInterface")
        .def("__gluecodium_id__", [](const CommentsInterface& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
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
            return self.some_method_with_all_comments(input);
        }, py::arg("input"))
        .def("some_method_with_input_comments", [](CommentsInterface& self, const ::std::string& input) {
            return self.some_method_with_input_comments(input);
        }, py::arg("input"))
        .def("some_method_with_output_comments", [](CommentsInterface& self, const ::std::string& input) {
            return self.some_method_with_output_comments(input);
        }, py::arg("input"))
        .def("some_method_with_no_comments", [](CommentsInterface& self, const ::std::string& input) {
            return self.some_method_with_no_comments(input);
        }, py::arg("input"))
        .def("some_method_without_return_type_with_all_comments", [](CommentsInterface& self, const ::std::string& input) {
            return self.some_method_without_return_type_with_all_comments(input);
        }, py::arg("input"))
        .def("some_method_without_return_type_with_no_comments", [](CommentsInterface& self, const ::std::string& input) {
            return self.some_method_without_return_type_with_no_comments(input);
        }, py::arg("input"))
        .def("some_method_without_input_parameters_with_all_comments", [](CommentsInterface& self) {
            return self.some_method_without_input_parameters_with_all_comments();
        })
        .def("some_method_without_input_parameters_with_no_comments", [](CommentsInterface& self) {
            return self.some_method_without_input_parameters_with_no_comments();
        })
        .def("some_method_with_nothing", [](CommentsInterface& self) {
            return self.some_method_with_nothing();
        })
        .def("some_method_without_return_type_or_input_parameters", [](CommentsInterface& self) {
            return self.some_method_without_return_type_or_input_parameters();
        })
        .def_property("is_some_property", [](const CommentsInterface& self) {
            return self.is_some_property();
        }, [](CommentsInterface& self, const bool value) {
            self.set_some_property(value);
        })
        ;
}

