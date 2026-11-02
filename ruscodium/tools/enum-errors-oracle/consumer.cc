#include "oracle/errors/Service.h"
#include "oracle/errors/RenamedError.h"
#include "oracle/errors/AuxiliaryOnly.h"
#include <cassert>
#include <string>
#include <system_error>
#include <type_traits>

using Service = oracle::errors::Service;
using Error = oracle::errors::RenamedError;
using Local = Service::LocalError;
using Other = Service::OtherError;
gluecodium::Return<int32_t, std::error_code> Service::refresh(bool fail) {
    if (fail) return std::error_code(Other::RETRY);
    return int32_t{17};
}
static_assert(std::is_error_code_enum<Error>::value);
static_assert(std::is_error_code_enum<Local>::value);
static_assert(!std::is_error_code_enum<oracle::errors::AuxiliaryOnly>::value);

class Concrete final : public Service {
public:
    std::error_code perform(bool fail) override {
        return fail ? std::error_code(Local::FAILED) : std::error_code{};
    }
    gluecodium::Return<int32_t, std::error_code> fetch(bool fail) override {
        if (fail) return std::error_code(Local::FAILED);
        return int32_t{42};
    }
    gluecodium::Return<gluecodium::optional<int32_t>, std::error_code> maybe(bool fail) override {
        if (fail) return std::error_code(Error::DENIED);
        return gluecodium::optional<int32_t>{19};
    }
};
int main() {
    const std::error_code local = Local::FAILED;
    assert(local.value() == 3 && std::string(local.category().name()) == "LocalErrorErrorCategory");
    assert(local.message() == "::oracle::errors::Service::LocalError::FAILED");
    const std::error_code unknown = static_cast<Local>(99);
    assert(unknown.message() == "Unknown enum value");
    const std::error_code global = Error::MISSING;
    assert(global.value() == 4 && std::string(global.category().name()) == "RenamedErrorErrorCategory");
    assert(global.message() == "::oracle::errors::RenamedError::MISSING");
    assert(Service::refresh(false).unsafe_value() == 17);
    assert(Service::refresh(true).error() == Other::RETRY);
    Concrete service;
    assert(!service.perform(false) && service.perform(true) == local);
    const auto value = service.fetch(false);
    const auto failure = service.fetch(true);
    assert(value.has_value() && value.unsafe_value() == 42);
    assert(!failure.has_value() && failure.error() == local);
    const auto maybe = service.maybe(false);
    const auto maybe_failure = service.maybe(true);
    assert(maybe.has_value() && maybe.unsafe_value() && *maybe.unsafe_value() == 19);
    assert(!maybe_failure.has_value() && maybe_failure.error() == Error::DENIED);
}
