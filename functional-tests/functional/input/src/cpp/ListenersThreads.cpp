// -------------------------------------------------------------------------------------------------
// Copyright (C) 2016-2019 HERE Europe B.V.
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

#include "test/ThreadedListener.h"
#include "test/ThreadedCallableListener.h"
#include "test/ThreadedDispatcher.h"
#include "test/ThreadedNotifier.h"
#include "test/UnloadedClass.h"

#include <exception>
#include <future>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

namespace test
{
namespace
{
void
notify_impl( const std::shared_ptr< ThreadedListener >& listener,
             const std::string& message,
             int64_t& response )
{
    listener->unloaded( UnloadedClass::create( ) );
    response = listener->on_event( message );
}

void
notify_no_response(const std::shared_ptr<ThreadedListener>& listener, const std::string& message) {
    listener->on_event(message);
}

void
notify_lambda_no_response(const std::function<void(const std::string&)>& lambda,
                          const std::string& message) {
    lambda(message);
}
}

class ThreadedNotifierImpl : public ThreadedNotifier
{
public:
    int64_t
    notify( const std::shared_ptr< ThreadedListener >& listener,
            const std::string& message ) override
    {
        int64_t response;
        std::exception_ptr error;
        std::thread notification_thread([&] {
            try {
                notify_impl(listener, message, response);
            } catch (...) {
                error = std::current_exception();
            }
        });
        notification_thread.join();
        if (error) std::rethrow_exception(error);
        return response;
    }

    void
    notify_on_detached(const std::shared_ptr<ThreadedListener>& listener,
                       const std::string& message) override {
        auto completion = add_completion();
        std::thread([held_listener = listener, message, completion]() mutable {
            try {
                notify_no_response(held_listener, message);
                held_listener.reset();
                completion->set_value();
            } catch (...) {
                held_listener.reset();
                completion->set_exception(std::current_exception());
            }
        }).detach();
    }

    void
    notify_lambda_on_detached(const std::function<void(const std::string&)>& lambda,
                              const std::string& message) override {
        auto completion = add_completion();
        std::thread([held_callback = lambda, message, completion]() mutable {
            try {
                notify_lambda_no_response(held_callback, message);
                held_callback = {};
                completion->set_value();
            } catch (...) {
                held_callback = {};
                completion->set_exception(std::current_exception());
            }
        }).detach();
    }

    void wait_for_callbacks() override {
        std::vector<std::future<void>> pending;
        {
            std::lock_guard<std::mutex> lock(m_mutex);
            pending.swap(m_completions);
        }
        std::exception_ptr first_error;
        for (auto& completion : pending) {
            try {
                completion.get();
            } catch (...) {
                if (!first_error) first_error = std::current_exception();
            }
        }
        if (first_error) std::rethrow_exception(first_error);
    }

private:
    std::shared_ptr<std::promise<void>> add_completion() {
        auto completion = std::make_shared<std::promise<void>>();
        std::lock_guard<std::mutex> lock(m_mutex);
        m_completions.push_back(completion->get_future());
        return completion;
    }

    std::mutex m_mutex;
    std::vector<std::future<void>> m_completions;
};

class ThreadedDispatcherImpl : public ThreadedDispatcher {
public:
    int64_t notify(const std::shared_ptr<ThreadedListener>& listener,
                   const std::string& message) override {
        ThreadedNotifierImpl notifier;
        return notifier.notify(listener, message);
    }
};

ThreadedNotifier::WorkerCallback
ThreadedNotifier::get_worker_callback() {
    return [](const std::shared_ptr<ThreadedListener>& listener, const std::string& message) {
        ThreadedNotifierImpl notifier;
        return notifier.notify(listener, message);
    };
}

lorem_ipsum::test::optional<ThreadedNotifier::WorkerCallback>
ThreadedNotifier::get_nullable_worker_callback(bool present) {
    if (present) return get_worker_callback();
    return {};
}

std::vector<lorem_ipsum::test::optional<ThreadedNotifier::WorkerCallback>>
ThreadedNotifier::get_worker_callbacks() {
    return {get_worker_callback(), {}};
}

ThreadedNotifier::CallbackHolder
ThreadedNotifier::get_callback_holder() {
    return CallbackHolder{get_worker_callback(), get_worker_callbacks()};
}

ThreadedNotifier::WorkerCallback
ThreadedNotifier::get_worker_operation() {
    return get_worker_callback();
}

int64_t
ThreadedNotifier::send_callback(const std::shared_ptr<ThreadedCallableListener>& listener) {
    return listener->accept(get_worker_callback());
}

void
ThreadedNotifier::set_callback(const std::shared_ptr<ThreadedCallableListener>& listener) {
    listener->set_callback(get_worker_callback());
}

lorem_ipsum::test::Return<ThreadedNotifier::WorkerCallback, std::error_code>
ThreadedNotifier::get_throwing_callback() {
    return get_worker_callback();
}

class UnloadedClassImpl : public UnloadedClass
{
public:
    virtual ~UnloadedClassImpl( ) = default;
    uint8_t increment( uint8_t in ) {
        return ++in;
    }
};

std::shared_ptr< UnloadedClass >
UnloadedClass::create( )
{
    return std::make_shared< UnloadedClassImpl >( );
}

std::shared_ptr<ThreadedDispatcher>
ThreadedNotifier::create_dispatcher() {
    return std::make_shared<ThreadedDispatcherImpl>();
}

std::shared_ptr< ThreadedNotifier >
ThreadedNotifier::create_on_new_thread( )
{
    return std::make_shared< ThreadedNotifierImpl >( );
}
}