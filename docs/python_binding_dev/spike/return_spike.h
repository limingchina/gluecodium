// Minimal standalone replica of Gluecodium's Return<T, Error> template.
// Mirrors the public API of gluecodium/.../templates/cpp/common/Return.mustache
// (operator bool, has_value, error, unsafe_value, safe_value) so the spike
// exercises the same surface a real pybind11 caster must handle.
#pragma once

#include <new>
#include <system_error>
#include <type_traits>
#include <utility>

template <class Value, class Error = std::error_code>
class Return {
public:
    using value_type = Value;
    using error_type = Error;

private:
    bool m_has_value;
    union {
        Value m_value;
        Error m_error;
    };

public:
    constexpr Return() noexcept : m_has_value(false), m_error(Error{}) {}
    Return(const Return& other) : m_has_value(other.m_has_value) {
        if (m_has_value) new (&m_value) Value(other.m_value);
        else new (&m_error) Error(other.m_error);
    }
    Return(Return&& other) : m_has_value(other.m_has_value) {
        if (m_has_value) new (&m_value) Value(std::move(other.m_value));
        else new (&m_error) Error(std::move(other.m_error));
        other.reset();
    }
    Return(const Value& value) : m_has_value(true), m_value(value) {}
    Return(Value&& value) : m_has_value(true), m_value(std::move(value)) {}
    Return(const Error& error) : m_has_value(false), m_error(error) {}
    Return(Error&& error) : m_has_value(false), m_error(std::move(error)) {}
    ~Return() { reset(); }

    explicit operator bool() const noexcept { return m_has_value; }
    bool has_value() const noexcept { return m_has_value; }
    Error error() const noexcept { return m_has_value ? Error{} : m_error; }

    const Value& unsafe_value() const& { return m_value; }
    Value unsafe_value() && { return std::move(m_value); }

    template <class Dummy = Value>
    typename std::enable_if<
        std::is_same<Dummy, Value>::value && std::is_constructible<Dummy>::value,
        Value>::type
    safe_value() const& {
        return m_has_value ? m_value : Value();
    }

private:
    void reset() noexcept {
        if (m_has_value) m_value.~Value();
        else m_error.~Error();
    }
};
