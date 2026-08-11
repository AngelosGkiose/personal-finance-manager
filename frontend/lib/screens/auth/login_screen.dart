import 'package:flutter/material.dart';

import '../../services/auth_service.dart';
import '../../storage/token_storage.dart';
import '../home/home_screen.dart';
import 'register_screen.dart';


class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() =>
      _LoginScreenState();
}


class _LoginScreenState
    extends State<LoginScreen> {

  final _formKey = GlobalKey<FormState>();

  final _emailController =
      TextEditingController();

  final _passwordController =
      TextEditingController();

  bool _isLoading = false;
  String? _errorMessage;
  String? _successMessage;


  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();

    super.dispose();
  }


  Future<void> _login() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
      _errorMessage = null;
      _successMessage = null;
    });

    try {
      final accessToken =
          await AuthService.login(
        email: _emailController.text.trim(),
        password: _passwordController.text,
      );

      await TokenStorage.saveAccessToken(
        accessToken,
      );

      if (!mounted) {
        return;
      }

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) =>
              const HomeScreen(),
        ),
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


  Future<void> _openRegisterScreen() async {
    final registered =
        await Navigator.push<bool>(
      context,
      MaterialPageRoute(
        builder: (context) =>
            const RegisterScreen(),
      ),
    );

    if (!mounted) {
      return;
    }

    if (registered == true) {
      setState(() {
        _successMessage =
            'Registration successful. Please log in.';

        _errorMessage = null;
      });
    }
  }


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Login'),
      ),

      body: Padding(
        padding: const EdgeInsets.all(16),

        child: Form(
          key: _formKey,

          child: Column(
            children: [
              TextFormField(
                controller:
                    _emailController,

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
                      value.isEmpty) {
                    return 'Password is required';
                  }

                  return null;
                },
              ),

              const SizedBox(height: 20),

              if (_errorMessage != null)
                Text(_errorMessage!),

              if (_successMessage != null)
                Text(_successMessage!),

              const SizedBox(height: 20),

              ElevatedButton(
                onPressed:
                    _isLoading ? null : _login,

                child: _isLoading
                    ? const CircularProgressIndicator()
                    : const Text('Login'),
              ),

              const SizedBox(height: 20),

              TextButton(
                onPressed:
                    _openRegisterScreen,

                child: const Text(
                  "Don't have an account? Register",
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}