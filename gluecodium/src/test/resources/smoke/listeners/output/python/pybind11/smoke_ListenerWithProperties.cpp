

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/CalculationResult.h"
#include "smoke/ListenerWithProperties.h"
#include "cstdint"
#include "memory"
#include "string"
#include "unordered_map"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ListenerWithProperties = ::smoke::ListenerWithProperties;

class ListenerWithPropertiesTrampoline : public ListenerWithProperties {
public:
    using ListenerWithProperties::ListenerWithProperties;

    // Holds an adopted native implementation (e.g. a C++ implementation of this interface
    // returned by a factory). When non-null, the trampoline forwards virtual calls to it
    // instead of the pure-virtual stub, so `RootInterface(native_result)` actually invokes
    // the returned implementation. A Python subclass is instantiated with no impl held, in
    // which case the overrides fall back to PYBIND11_OVERRIDE_PURE for Python dispatch.
    std::shared_ptr<ListenerWithProperties> m_impl;

    ::std::string get_message() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_message();
        }
        PYBIND11_OVERRIDE_PURE(::std::string, ListenerWithProperties, get_message);
    }
    void set_message(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_message(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ListenerWithProperties, set_message, value);
    }
    ::std::shared_ptr< ::smoke::CalculationResult > get_packed_message() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_packed_message();
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::CalculationResult >, ListenerWithProperties, get_packed_message);
    }
    void set_packed_message(const ::std::shared_ptr< ::smoke::CalculationResult >& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_packed_message(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ListenerWithProperties, set_packed_message, value);
    }
    ::smoke::ListenerWithProperties::ResultStruct get_structured_message() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_structured_message();
        }
        PYBIND11_OVERRIDE_PURE(::smoke::ListenerWithProperties::ResultStruct, ListenerWithProperties, get_structured_message);
    }
    void set_structured_message(const ::smoke::ListenerWithProperties::ResultStruct& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_structured_message(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ListenerWithProperties, set_structured_message, value);
    }
    ::smoke::ListenerWithProperties::ResultEnum get_enumerated_message() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_enumerated_message();
        }
        PYBIND11_OVERRIDE_PURE(::smoke::ListenerWithProperties::ResultEnum, ListenerWithProperties, get_enumerated_message);
    }
    void set_enumerated_message(const ::smoke::ListenerWithProperties::ResultEnum value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_enumerated_message(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ListenerWithProperties, set_enumerated_message, value);
    }
    ::std::vector< ::std::string > get_arrayed_message() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_arrayed_message();
        }
        PYBIND11_OVERRIDE_PURE(::std::vector< ::std::string >, ListenerWithProperties, get_arrayed_message);
    }
    void set_arrayed_message(const ::std::vector< ::std::string >& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_arrayed_message(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ListenerWithProperties, set_arrayed_message, value);
    }
    using get_mapped_message_return_type = ::std::unordered_map< ::std::string, double >;
    ::std::unordered_map< ::std::string, double > get_mapped_message() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_mapped_message();
        }
        PYBIND11_OVERRIDE_PURE(get_mapped_message_return_type, ListenerWithProperties, get_mapped_message);
    }
    void set_mapped_message(const ::std::unordered_map< ::std::string, double >& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_mapped_message(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ListenerWithProperties, set_mapped_message, value);
    }
    ::std::shared_ptr< ::std::vector< uint8_t > > get_buffered_message() const override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            return m_impl->get_buffered_message();
        }
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::std::vector< uint8_t > >, ListenerWithProperties, get_buffered_message);
    }
    void set_buffered_message(const ::std::shared_ptr< ::std::vector< uint8_t > >& value) override {
        py::gil_scoped_acquire gil;
        if (m_impl) {
            m_impl->set_buffered_message(value);
            return;
        }
        PYBIND11_OVERRIDE_PURE(void, ListenerWithProperties, set_buffered_message, value);
    }
};

void register_smoke_ListenerWithProperties(py::module_& module) {
    py::class_<ListenerWithProperties, std::shared_ptr<ListenerWithProperties>, ListenerWithPropertiesTrampoline>(module, "ListenerWithProperties")
        .def(py::init<>())
        // Adoption constructor: when a factory returns an existing native instance (e.g. a
        // C++ implementation of this interface), adopt it into the trampoline subclass and
        // stash it in `m_impl` so virtual calls forward to the real implementation instead
        // of the pure-virtual stub. `init_alias` cannot be used here because the returned
        // instance is a foreign (non-trampoline) implementation; instead we build a fresh
        // trampoline and store the impl directly.
        .def(py::init([](std::shared_ptr<ListenerWithProperties> native) {
            auto self = std::make_shared<ListenerWithPropertiesTrampoline>();
            self->m_impl = native;
            return self;
        }))
        .def_property("message", [](const ListenerWithProperties& self) {
            return self.get_message();
        }, [](ListenerWithProperties& self, const ::std::string& value) {
            self.set_message(value);
        })
        .def_property("packed_message", [](const ListenerWithProperties& self) {
            return self.get_packed_message();
        }, [](ListenerWithProperties& self, const ::std::shared_ptr< ::smoke::CalculationResult >& value) {
            self.set_packed_message(value);
        })
        .def_property("structured_message", [](const ListenerWithProperties& self) {
            return self.get_structured_message();
        }, [](ListenerWithProperties& self, const ::smoke::ListenerWithProperties::ResultStruct& value) {
            self.set_structured_message(value);
        })
        .def_property("enumerated_message", [](const ListenerWithProperties& self) {
            return self.get_enumerated_message();
        }, [](ListenerWithProperties& self, const ::smoke::ListenerWithProperties::ResultEnum value) {
            self.set_enumerated_message(value);
        })
        .def_property("arrayed_message", [](const ListenerWithProperties& self) {
            return self.get_arrayed_message();
        }, [](ListenerWithProperties& self, const ::std::vector< ::std::string >& value) {
            self.set_arrayed_message(value);
        })
        .def_property("mapped_message", [](const ListenerWithProperties& self) {
            return self.get_mapped_message();
        }, [](ListenerWithProperties& self, const ::std::unordered_map< ::std::string, double >& value) {
            self.set_mapped_message(value);
        })
        .def_property("buffered_message", [](const ListenerWithProperties& self) {
            return self.get_buffered_message();
        }, [](ListenerWithProperties& self, const ::std::shared_ptr< ::std::vector< uint8_t > >& value) {
            self.set_buffered_message(value);
        })
        ;
}

