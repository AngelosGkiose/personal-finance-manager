import 'package:flutter/material.dart';

import '../../services/auth_service.dart';


class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() =>
      _RegisterScreenState();
}


class _RegisterScreenState
    extends State<RegisterScreen> {

  final _formKey = GlobalKey<FormState>();

  final _usernameController =
      TextEditingController();

  final _emailController =
      TextEditingController();

  final _passwordController =
      TextEditingController();

  bool _isLoading = false;
  String? _errorMessage;


  @override
  void dispose() {
    _usernameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();

    super.dispose();
  }


  Future<void> _register() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    try {
      await AuthService.register(
        username:
            _usernameController.text.trim(),
        email:
            _emailController.text.trim(),
        password:
            _passwordController.text,
      );

      if (!mounted) {
        return;
      }

      Navigator.pop(
        context,
        true,
      );

    } catch (error) {
      if (!mounted) {
        return;
      }

      setState(() {
        _errorMessage = error
            .toString()
            .replaceFirst('Exception: ', '');
      });

    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Register'),
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,

          child: Column(
            children: [
              TextFormField(
                controller:
                    _usernameController,
                decoration:
                    const InputDecoration(
                  labelText: 'Username',
                ),
                validator: (value) {
                  if (value == null ||
                      value.trim().isEmpty) {
                    return 'Username is required';
                  }

                  return null;
                },
              ),

              TextFormField(
                controller: _emailController,
                keyboardType:
                    TextInputType.emailAddress,
                decoration:
                    const InputDecoration(
                  labelText: 'Email',
                ),
                validator: (value) {
                  if (value == null ||
                      value.trim().isEmpty) {
                    return 'Email is required';
                  }

                  return null;
                },
              ),

              TextFormField(
                controller:
                    _passwordController,
                obscureText: true,
                decoration:
                    const InputDecoration(
                  labelText: 'Password',
                ),
                validator: (value) {
                  if (value == null ||
                      value.length < 8) {
                    return 'Password must be at least 8 characters';
                  }

                  return null;
                },
              ),

              const SizedBox(height: 20),

              if (_errorMessage != null)
                Text(_errorMessage!),

              const SizedBox(height: 20),

              ElevatedButton(
                onPressed:
                    _isLoading ? null : _register,
                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text('Register'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}