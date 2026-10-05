// -------------------------------------------------------------------------------------------------
// Copyright (C) 2016-2020 HERE Europe B.V.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// SPDX-License-Identifier: Apache-2.0
// License-Filename: LICENSE
//
// -------------------------------------------------------------------------------------------------

#include "test/DummyChildClass.h"
#include "test/DummyClass.h"
#include "test/DummyParentClass.h"
#include "test/DummyFactory.h"
#include "test/DummyInterface.h"
#include "test/DummyChildInterface.h"

#include <atomic>
#include <new>
#include <stdexcept>

namespace test
{
namespace {
std::atomic<int64_t> s_live_count{0};
std::atomic<int64_t> s_destroyed_count{0};
std::atomic<int64_t> s_generation{0};

class TrackedLifetime {
public:
    TrackedLifetime() : generation(++s_generation) { ++s_live_count; }
    ~TrackedLifetime() { --s_live_count; ++s_destroyed_count; }
    const int64_t generation;
};

class DummyClassImpl : public DummyClass, public TrackedLifetime {
public:
    ~DummyClassImpl() = default;
};

class DummyInterfaceImpl : public DummyInterface, public TrackedLifetime {
public:
    ~DummyInterfaceImpl() = default;
};

class DummyChildInterfaceImpl : public DummyChildInterface, public TrackedLifetime {
public:
    ~DummyChildInterfaceImpl() = default;
};

class DummyChildClassImpl : public DummyChildClass, public TrackedLifetime {
public:
    ~DummyChildClassImpl() = default;
};

alignas(DummyClassImpl) unsigned char s_reused_storage[sizeof(DummyClassImpl)];
std::atomic<bool> s_reused_occupied{false};

std::shared_ptr<DummyClass> s_dummy_class = std::make_shared<DummyClassImpl>();
std::shared_ptr<DummyInterface> s_dummy_interface = std::make_shared<DummyInterfaceImpl>();
std::shared_ptr<DummyChildInterface> s_dummy_child_interface = std::make_shared<DummyChildInterfaceImpl>();
std::shared_ptr<DummyChildClass> s_dummy_child_class = std::make_shared<DummyChildClassImpl>();
}

std::shared_ptr<DummyClass>
DummyClass::create() {
    return std::make_shared<DummyClassImpl>();
}

std::shared_ptr<DummyClass>
DummyClass::dummy_class_round_trip(const std::shared_ptr<DummyClass>& input) {
    return input;
}

std::vector<std::shared_ptr<DummyClass>>
DummyClass::dummy_class_list_round_trip(const std::vector<std::shared_ptr<DummyClass>>& input) {
    return input;
}

int64_t DummyFactory::get_native_live_count() { return s_live_count.load(); }
int64_t DummyFactory::get_native_destroyed_count() { return s_destroyed_count.load(); }
int64_t DummyFactory::get_native_generation(const std::shared_ptr<DummyClass>& instance) {
    return dynamic_cast<const DummyClassImpl&>(*instance).generation;
}

std::shared_ptr<DummyClass>
DummyFactory::create_reused_dummy_class() {
    if (s_reused_occupied.exchange(true)) {
        throw std::runtime_error("Previous reused object is still alive");
    }
    auto* instance = new (s_reused_storage) DummyClassImpl();
    return std::shared_ptr<DummyClass>(instance, [](DummyClass* value) {
        static_cast<DummyClassImpl*>(value)->~DummyClassImpl();
        s_reused_occupied = false;
    });
}

std::shared_ptr<DummyClass>
DummyFactory::get_dummy_class_singleton() {
    return s_dummy_class;
}

std::shared_ptr<DummyClass>
DummyFactory::create_dummy_class() {
    return std::make_shared<DummyClassImpl>();
}

std::shared_ptr<DummyInterface>
DummyFactory::get_dummy_interface_singleton() {
    return s_dummy_interface;
}

std::shared_ptr<DummyInterface>
DummyFactory::create_dummy_interface() {
    return std::make_shared<DummyInterfaceImpl>();
}

std::shared_ptr<DummyChildInterface>
DummyFactory::get_dummy_child_interface_singleton() {
    return s_dummy_child_interface;
}

std::shared_ptr<DummyInterface>
DummyFactory::get_dummy_child_interface_singleton_as_parent() {
    return s_dummy_child_interface;
}

std::shared_ptr<DummyChildClass>
DummyFactory::get_dummy_child_class_singleton() {
    return s_dummy_child_class;
}

std::shared_ptr<DummyParentClass>
DummyFactory::get_dummy_child_class_singleton_as_parent() {
    return s_dummy_child_class;
}

}
